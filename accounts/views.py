from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from .forms import UserRegistrationForm, UserProfileForm, OTPVerificationForm
from .utils import send_otp_email, verify_otp

def _make_unique_username(base):
    import re
    slug = re.sub(r'[^a-z0-9._]', '', base.lower().replace(' ', '.'))[:28] or 'user'
    username, n = slug, 1
    while CustomUser.objects.filter(username=username).exists():
        username = f"{slug}{n}"
        n += 1
    return username


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Unique username — auto-suffix if taken
            user.username = _make_unique_username(form.cleaned_data.get('username', ''))

            # Unique email — show friendly error if taken
            email = form.cleaned_data.get('email', '').strip().lower()
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered. Please login instead.')
                return render(request, 'accounts/register.html', {'form': form})
            user.email = email

            # Unique phone — store None if already taken (don't crash)
            phone = form.cleaned_data.get('phone_number', '').strip()
            user.phone_number = phone if phone and not CustomUser.objects.filter(phone_number=phone).exists() else None

            user.is_active = True
            user.is_verified = True
            user.save()

            login(request, user)
            messages.success(request, 'Registration successful! Welcome to TravelVibe!')
            return redirect('homepage')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_otp_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('register')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            if verify_otp(user, otp_code):
                user.is_active = True
                user.is_verified = True
                user.save()
                login(request, user)
                del request.session['user_id']
                messages.success(request, 'Email verified successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid or expired OTP.')
    else:
        form = OTPVerificationForm()
    return render(request, 'accounts/verify_otp.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            username = username.lower().replace(' ', '.')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Remove email verification requirement
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required
def profile_view(request):
    # Get user's bookings with related data
    from bookings.models import Booking
    
    bookings = Booking.objects.filter(user=request.user).select_related('package', 'package__destination').prefetch_related('travelers', 'payments')
    
    if request.method == 'POST':
        user = request.user
        user.first_name      = request.POST.get('first_name', '').strip()
        user.last_name       = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone_number', '').strip()
        user.phone_number    = phone if phone else None
        user.passport_number = request.POST.get('passport_number', '').strip() or None
        user.address         = request.POST.get('address', '').strip()
        user.aadhar_number   = request.POST.get('aadhar_number', '').strip()
        expiry = request.POST.get('passport_expiry', '').strip()
        if expiry:
            try:
                from datetime import datetime
                user.passport_expiry = datetime.strptime(expiry, '%Y-%m-%d').date()
            except ValueError:
                pass
        try:
            user.save(update_fields=[
                'first_name', 'last_name', 'phone_number', 'passport_number',
                'passport_expiry', 'address', 'aadhar_number'
            ])
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Could not save profile: {e}')
        return redirect('profile')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'accounts/profile.html', context)

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.scheme}://{request.get_host()}/accounts/reset-password/{uid}/{token}/"

            # Try sending email — silently skip if email not configured
            try:
                from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@travelvibe.com'
                send_mail(
                    'TravelVibe - Password Reset',
                    f'Click the link to reset your password: {reset_link}',
                    from_email,
                    [email],
                    fail_silently=True,
                )
            except Exception:
                pass

            # Always show the link in the success message (dev-friendly)
            messages.success(request, 'Password reset link ready.')
            request.session['reset_link'] = reset_link
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with that email address.')
    return render(request, 'accounts/forgot_password.html')

def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password reset successful! Please login.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'accounts/reset_password.html')
    else:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('forgot_password')

def accounts_report_view(request):
    from bookings.models import Booking
    from store.models import TourPackage, Destination
    from django.db.models import Sum, Count
    from django.utils import timezone
    from datetime import timedelta

    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()

    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    seven_days_ago  = now - timedelta(days=7)

    accounts = CustomUser.objects.all().order_by('-date_joined')
    bookings = Booking.objects.select_related('user', 'package', 'package__destination').order_by('-created_at')

    # Revenue stats
    total_revenue   = bookings.aggregate(t=Sum('total_amount'))['t'] or 0
    total_collected = bookings.aggregate(t=Sum('amount_paid'))['t'] or 0
    total_pending   = bookings.aggregate(t=Sum('remaining_amount'))['t'] or 0

    # Booking status counts
    confirmed_count  = bookings.filter(status='confirmed').count()
    pending_count    = bookings.filter(status='pending').count()
    cancelled_count  = bookings.filter(status='cancelled').count()
    completed_count  = bookings.filter(status='completed').count()

    # Recent activity
    new_bookings_7d  = bookings.filter(created_at__gte=seven_days_ago).count()
    new_users_30d    = accounts.filter(date_joined__gte=thirty_days_ago, is_staff=False).count()

    # Top destinations
    top_destinations = (
        bookings.values('package__destination__name')
        .annotate(count=Count('id'), revenue=Sum('total_amount'))
        .order_by('-count')[:5]
    )

    # Recent 8 bookings for activity feed
    recent_bookings = bookings[:8]

    context = {
        'accounts': accounts,
        'total_accounts': accounts.count(),
        'admins_count': accounts.filter(is_staff=True).count(),
        'users_count': accounts.filter(is_staff=False).count(),
        'new_users_30d': new_users_30d,
        'total_bookings': bookings.count(),
        'confirmed_count': confirmed_count,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,
        'new_bookings_7d': new_bookings_7d,
        'total_revenue': total_revenue,
        'total_collected': total_collected,
        'total_pending': total_pending,
        'top_destinations': top_destinations,
        'recent_bookings': recent_bookings,
        'total_packages': TourPackage.objects.count(),
        'total_destinations': Destination.objects.count(),
    }
    return render(request, 'accounts/accounts_report.html', context)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='login')
def booking_report_view(request):
    from bookings.models import Booking
    from django.db.models import Sum

    bookings = (
        Booking.objects
        .select_related('user', 'package', 'package__destination')
        .prefetch_related('travelers')
        .order_by('-created_at')
    )

    total_revenue   = bookings.aggregate(t=Sum('total_amount'))['t'] or 0
    total_collected = bookings.aggregate(t=Sum('amount_paid'))['t'] or 0
    total_pending   = bookings.aggregate(t=Sum('remaining_amount'))['t'] or 0

    context = {
        'bookings': bookings,
        'total_revenue': total_revenue,
        'total_collected': total_collected,
        'total_pending': total_pending,
    }
    return render(request, 'accounts/booking_report.html', context)
