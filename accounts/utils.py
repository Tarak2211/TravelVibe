import random
from django.core.mail import send_mail
from django.conf import settings
from .models import OTPVerification

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user):
    otp_code = generate_otp()
    OTPVerification.objects.create(user=user, otp_code=otp_code)
    
    subject = 'TravelVibe - Your OTP Code'
    message = f'Your OTP code is: {otp_code}\n\nThis code will expire in 10 minutes.'
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return otp_code

def verify_otp(user, otp_code):
    try:
        otp = OTPVerification.objects.filter(
            user=user, 
            otp_code=otp_code, 
            is_used=False
        ).latest('created_at')
        
        if otp.is_valid():
            otp.is_used = True
            otp.save()
            return True
    except OTPVerification.DoesNotExist:
        pass
    return False
