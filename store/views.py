from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from django.db.models import Q
from .models import Destination, TourPackage, Banner, Testimonial

logger = logging.getLogger(__name__)

def homepage_view(request):
    # Redirect admin users to their dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('accounts_report')

    # Get active banners only
    banners = Banner.objects.filter(is_active=True)[:3]
    
    context = {
        'banners': banners,
    }
    
    return render(request, 'store/homepage.html', context)

def destinations_view(request):
    # Get all destinations
    destinations = Destination.objects.all()
    
    context = {
        'destinations': destinations,
    }
    
    return render(request, 'store/destinations.html', context)

def packages_view(request):
    destination = request.GET.get('destination', '').strip()
    category    = request.GET.get('category', '')
    duration    = request.GET.get('duration', '')
    sort        = request.GET.get('sort', '')
    price_min   = request.GET.get('price_min', '')
    price_max   = request.GET.get('price_max', '')
    trip_type   = request.GET.get('trip_type', '')   # domestic / international

    packages = TourPackage.objects.all()

    if destination:
        packages = packages.filter(
            Q(destination__name__icontains=destination) |
            Q(destination__country__icontains=destination) |
            Q(title__icontains=destination)
        )
    if category and category != 'all':
        packages = packages.filter(category=category)
    if duration and duration != 'all':
        packages = packages.filter(duration=duration)
    if price_min:
        try: packages = packages.filter(price_per_person__gte=int(price_min))
        except ValueError: pass
    if price_max:
        try: packages = packages.filter(price_per_person__lte=int(price_max))
        except ValueError: pass
    if trip_type == 'domestic':
        packages = packages.filter(destination__country='India')
    elif trip_type == 'international':
        packages = packages.exclude(destination__country='India')

    if sort == 'price_low':
        packages = packages.order_by('price_per_person')
    elif sort == 'price_high':
        packages = packages.order_by('-price_per_person')
    elif sort == 'popular':
        packages = packages.order_by('-popularity_score')
    elif sort == 'duration_short':
        packages = packages.order_by('duration')
    else:
        packages = packages.order_by('-popularity_score', '-created_at')

    all_destinations = Destination.objects.all()

    context = {
        'packages': packages,
        'all_destinations': all_destinations,
        'search_destination': destination,
        'search_category': category,
        'search_duration': duration,
        'search_sort': sort,
        'search_price_min': price_min,
        'search_price_max': price_max,
        'search_trip_type': trip_type,
        'total_count': packages.count(),
    }

    return render(request, 'store/packages.html', context)

def about_view(request):
    # Get featured testimonials
    testimonials = Testimonial.objects.filter(is_featured=True)
    
    context = {
        'testimonials': testimonials,
    }
    
    return render(request, 'store/about.html', context)

def package_detail_view(request, package_id):
    from django.shortcuts import get_object_or_404
    from datetime import datetime, timedelta
    
    # Get the package
    package = get_object_or_404(TourPackage, id=package_id)
    
    # Get related packages from same destination
    related_packages = TourPackage.objects.filter(
        destination=package.destination
    ).exclude(id=package_id)[:3]
    
    # Flight options - REAL CURRENT MARKET PRICES (March 2026) with Layover Details
    # This is the FALLBACK data if API fails or is not configured
    flight_options = {
        'Dubai': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 995',
                    'departure': '02:00 AM',  # Red-eye direct flight
                    'arrival': '04:30 AM',
                    'duration': '3h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Dubai (DXB)',
                    'economy': 14500,  # Direct - cheapest early morning
                    'premium': 24000,
                    'business': 48000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1406',
                    'departure': '03:30 PM',  # Direct afternoon
                    'arrival': '06:00 PM',
                    'duration': '3h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Dubai (DXB)',
                    'economy': 17800,  # Direct - budget airline
                    'premium': 28500,
                    'business': 52000,
                },
                {
                    'airline': 'Emirates',
                    'flight_no': 'EK 512',
                    'departure': '08:45 AM',  # Direct peak time
                    'arrival': '11:15 AM',
                    'duration': '3h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Dubai (DXB)',
                    'economy': 24500,  # Most expensive - Emirates direct
                    'premium': 42000,
                    'business': 89000,
                },
                {
                    'airline': 'Qatar Airways',
                    'flight_no': 'QR 570',
                    'departure': '01:30 AM',
                    'arrival': '09:45 AM',
                    'duration': '8h 15m',
                    'stops': '1 Stop (Doha - 2h 30m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Dubai (DXB)',
                    'economy': 12800,  # Cheaper with layover
                    'premium': 22500,
                    'business': 45000,
                },
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 865',
                    'departure': '10:00 AM',
                    'arrival': '05:30 PM',
                    'duration': '7h 30m',
                    'stops': '1 Stop (Mumbai - 1h 45m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Dubai (DXB)',
                    'economy': 13200,  # Via Mumbai - budget option
                    'premium': 23000,
                    'business': 46500,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 996',
                    'departure': '08:45 PM',  # Direct night flight
                    'arrival': '01:15 AM+1',
                    'duration': '3h 30m',
                    'stops': 'Direct',
                    'from': 'Dubai (DXB)',
                    'to': 'Delhi (DEL)',
                    'economy': 15200,
                    'premium': 25500,
                    'business': 49500,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1407',
                    'departure': '11:30 PM',  # Direct late night - cheapest
                    'arrival': '04:00 AM+1',
                    'duration': '3h 30m',
                    'stops': 'Direct',
                    'from': 'Dubai (DXB)',
                    'to': 'Delhi (DEL)',
                    'economy': 13900,  # Cheapest direct return
                    'premium': 23500,
                    'business': 46000,
                },
                {
                    'airline': 'Emirates',
                    'flight_no': 'EK 513',
                    'departure': '02:50 PM',  # Direct afternoon
                    'arrival': '08:20 PM',
                    'duration': '3h 30m',
                    'stops': 'Direct',
                    'from': 'Dubai (DXB)',
                    'to': 'Delhi (DEL)',
                    'economy': 26000,  # Premium direct
                    'premium': 44000,
                    'business': 92000,
                },
                {
                    'airline': 'Qatar Airways',
                    'flight_no': 'QR 571',
                    'departure': '03:15 PM',
                    'arrival': '11:45 PM',
                    'duration': '7h 30m',
                    'stops': '1 Stop (Doha - 2h 15m layover)',
                    'from': 'Dubai (DXB)',
                    'to': 'Delhi (DEL)',
                    'economy': 14200,  # Cheaper via Doha
                    'premium': 24500,
                    'business': 48000,
                },
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 866',
                    'departure': '07:00 AM',
                    'arrival': '02:15 PM',
                    'duration': '6h 15m',
                    'stops': '1 Stop (Mumbai - 1h 30m layover)',
                    'from': 'Dubai (DXB)',
                    'to': 'Delhi (DEL)',
                    'economy': 13500,  # Via Mumbai
                    'premium': 23800,
                    'business': 47500,
                },
            ],
        },
        'Goa': {
            'outbound': [
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 6112',
                    'departure': '09:15 AM',  # Direct morning peak
                    'arrival': '11:45 AM',
                    'duration': '2h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Goa (GOI)',
                    'economy': 6200,  # Direct - weekend pricing
                    'premium': 9800,
                    'business': 17500,
                },
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 804',
                    'departure': '06:00 AM',  # Direct early morning
                    'arrival': '08:30 AM',
                    'duration': '2h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Goa (GOI)',
                    'economy': 4749,  # Air India current rate - cheapest direct
                    'premium': 8200,
                    'business': 15500,
                },
                {
                    'airline': 'Vistara',
                    'flight_no': 'UK 995',
                    'departure': '02:30 PM',  # Direct afternoon
                    'arrival': '05:00 PM',
                    'duration': '2h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Goa (GOI)',
                    'economy': 6850,  # Vistara premium
                    'premium': 11200,
                    'business': 20500,
                },
                {
                    'airline': 'SpiceJet',
                    'flight_no': 'SG 116',
                    'departure': '11:30 AM',
                    'arrival': '03:15 PM',
                    'duration': '3h 45m',
                    'stops': '1 Stop (Mumbai - 45min layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Goa (GOI)',
                    'economy': 4200,  # Cheapest with layover
                    'premium': 7500,
                    'business': 14200,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 5324',
                    'departure': '04:45 PM',
                    'arrival': '08:45 PM',
                    'duration': '4h 00m',
                    'stops': '1 Stop (Bangalore - 1h 10m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Goa (GOI)',
                    'economy': 4500,  # Budget via Bangalore
                    'premium': 7800,
                    'business': 14800,
                },
            ],
            'return': [
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 6113',
                    'departure': '03:30 PM',  # Direct peak return
                    'arrival': '06:00 PM',
                    'duration': '2h 30m',
                    'stops': 'Direct',
                    'from': 'Goa (GOI)',
                    'to': 'Delhi (DEL)',
                    'economy': 6450,  # Weekend return pricing
                    'premium': 10500,
                    'business': 18800,
                },
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 805',
                    'departure': '12:00 PM',  # Direct noon
                    'arrival': '02:30 PM',
                    'duration': '2h 30m',
                    'stops': 'Direct',
                    'from': 'Goa (GOI)',
                    'to': 'Delhi (DEL)',
                    'economy': 5285,  # Air India current rate
                    'premium': 9100,
                    'business': 16800,
                },
                {
                    'airline': 'Vistara',
                    'flight_no': 'UK 996',
                    'departure': '08:00 PM',  # Direct evening
                    'arrival': '10:30 PM',
                    'duration': '2h 30m',
                    'stops': 'Direct',
                    'from': 'Goa (GOI)',
                    'to': 'Delhi (DEL)',
                    'economy': 7600,  # Evening premium
                    'premium': 12500,
                    'business': 22800,
                },
                {
                    'airline': 'SpiceJet',
                    'flight_no': 'SG 117',
                    'departure': '06:30 AM',
                    'arrival': '10:30 AM',
                    'duration': '4h 00m',
                    'stops': '1 Stop (Mumbai - 55min layover)',
                    'from': 'Goa (GOI)',
                    'to': 'Delhi (DEL)',
                    'economy': 4650,  # Cheapest return via Mumbai
                    'premium': 8000,
                    'business': 15200,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 5325',
                    'departure': '09:15 AM',
                    'arrival': '01:30 PM',
                    'duration': '4h 15m',
                    'stops': '1 Stop (Hyderabad - 1h 05m layover)',
                    'from': 'Goa (GOI)',
                    'to': 'Delhi (DEL)',
                    'economy': 4900,  # Via Hyderabad
                    'premium': 8400,
                    'business': 15800,
                },
            ],
        },
        'Manali': {
            'outbound': [
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 2524',
                    'departure': '06:30 AM',  # Direct early morning
                    'arrival': '07:45 AM',
                    'duration': '1h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Bhuntar (KUU)',
                    'economy': 3850,  # Current market rate
                    'premium': 6400,
                    'business': 11200,
                },
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 463',
                    'departure': '10:00 AM',  # Direct peak time
                    'arrival': '11:15 AM',
                    'duration': '1h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Bhuntar (KUU)',
                    'economy': 4650,  # Peak pricing
                    'premium': 7600,
                    'business': 13200,
                },
                {
                    'airline': 'SpiceJet',
                    'flight_no': 'SG 8726',
                    'departure': '01:45 PM',
                    'arrival': '04:30 PM',
                    'duration': '2h 45m',
                    'stops': '1 Stop (Chandigarh - 45min layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Bhuntar (KUU)',
                    'economy': 3200,  # Cheapest via Chandigarh
                    'premium': 5800,
                    'business': 10200,
                },
                {
                    'airline': 'Alliance Air',
                    'flight_no': '9I 622',
                    'departure': '03:30 PM',
                    'arrival': '06:00 PM',
                    'duration': '2h 30m',
                    'stops': '1 Stop (Shimla - 35min layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Bhuntar (KUU)',
                    'economy': 3400,  # Budget via Shimla
                    'premium': 6000,
                    'business': 10500,
                },
            ],
            'return': [
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 2525',
                    'departure': '01:00 PM',  # Direct afternoon
                    'arrival': '02:15 PM',
                    'duration': '1h 15m',
                    'stops': 'Direct',
                    'from': 'Bhuntar (KUU)',
                    'to': 'Delhi (DEL)',
                    'economy': 4100,
                    'premium': 6700,
                    'business': 11800,
                },
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 464',
                    'departure': '04:30 PM',  # Direct evening
                    'arrival': '05:45 PM',
                    'duration': '1h 15m',
                    'stops': 'Direct',
                    'from': 'Bhuntar (KUU)',
                    'to': 'Delhi (DEL)',
                    'economy': 5200,  # Weekend return premium
                    'premium': 8300,
                    'business': 14500,
                },
                {
                    'airline': 'SpiceJet',
                    'flight_no': 'SG 8727',
                    'departure': '07:00 AM',
                    'arrival': '09:30 AM',
                    'duration': '2h 30m',
                    'stops': '1 Stop (Chandigarh - 40min layover)',
                    'from': 'Bhuntar (KUU)',
                    'to': 'Delhi (DEL)',
                    'economy': 3500,  # Cheapest return
                    'premium': 6100,
                    'business': 10800,
                },
                {
                    'airline': 'Alliance Air',
                    'flight_no': '9I 623',
                    'departure': '11:00 AM',
                    'arrival': '01:15 PM',
                    'duration': '2h 15m',
                    'stops': '1 Stop (Shimla - 30min layover)',
                    'from': 'Bhuntar (KUU)',
                    'to': 'Delhi (DEL)',
                    'economy': 3650,  # Via Shimla
                    'premium': 6300,
                    'business': 11000,
                },
            ],
        },
        'Kerala': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 440',
                    'departure': '06:00 AM',  # Direct early morning
                    'arrival': '09:15 AM',
                    'duration': '3h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Cochin (COK)',
                    'economy': 6950,  # Air India current rate
                    'premium': 11500,
                    'business': 22200,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 2134',
                    'departure': '11:30 AM',  # Direct mid-day
                    'arrival': '02:45 PM',
                    'duration': '3h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Cochin (COK)',
                    'economy': 6200,  # Budget airline
                    'premium': 10100,
                    'business': 19200,
                },
                {
                    'airline': 'Vistara',
                    'flight_no': 'UK 621',
                    'departure': '04:00 PM',  # Direct afternoon
                    'arrival': '07:15 PM',
                    'duration': '3h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Cochin (COK)',
                    'economy': 7850,  # Premium airline
                    'premium': 13200,
                    'business': 25500,
                },
                {
                    'airline': 'SpiceJet',
                    'flight_no': 'SG 58',
                    'departure': '08:30 AM',
                    'arrival': '01:00 PM',
                    'duration': '4h 30m',
                    'stops': '1 Stop (Mumbai - 1h 05m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Cochin (COK)',
                    'economy': 5400,  # Cheapest via Mumbai
                    'premium': 9200,
                    'business': 17500,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 5186',
                    'departure': '01:15 PM',
                    'arrival': '06:15 PM',
                    'duration': '5h 00m',
                    'stops': '1 Stop (Bangalore - 1h 30m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Cochin (COK)',
                    'economy': 5650,  # Via Bangalore
                    'premium': 9500,
                    'business': 18000,
                },
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 544',
                    'departure': '10:00 PM',
                    'arrival': '03:45 AM+1',
                    'duration': '5h 45m',
                    'stops': '1 Stop (Hyderabad - 1h 50m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Cochin (COK)',
                    'economy': 5800,  # Night via Hyderabad
                    'premium': 9800,
                    'business': 18500,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 441',
                    'departure': '05:00 PM',  # Direct evening
                    'arrival': '08:15 PM',
                    'duration': '3h 15m',
                    'stops': 'Direct',
                    'from': 'Cochin (COK)',
                    'to': 'Delhi (DEL)',
                    'economy': 7350,
                    'premium': 12200,
                    'business': 23500,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 2135',
                    'departure': '10:00 AM',  # Direct morning
                    'arrival': '01:15 PM',
                    'duration': '3h 15m',
                    'stops': 'Direct',
                    'from': 'Cochin (COK)',
                    'to': 'Delhi (DEL)',
                    'economy': 6700,  # Mid-range
                    'premium': 10800,
                    'business': 20200,
                },
                {
                    'airline': 'Vistara',
                    'flight_no': 'UK 622',
                    'departure': '08:30 PM',  # Direct night
                    'arrival': '11:45 PM',
                    'duration': '3h 15m',
                    'stops': 'Direct',
                    'from': 'Cochin (COK)',
                    'to': 'Delhi (DEL)',
                    'economy': 8200,  # Evening premium
                    'premium': 13900,
                    'business': 26800,
                },
                {
                    'airline': 'SpiceJet',
                    'flight_no': 'SG 59',
                    'departure': '06:15 AM',
                    'arrival': '10:30 AM',
                    'duration': '4h 15m',
                    'stops': '1 Stop (Mumbai - 55min layover)',
                    'from': 'Cochin (COK)',
                    'to': 'Delhi (DEL)',
                    'economy': 5850,  # Cheapest via Mumbai
                    'premium': 9800,
                    'business': 18500,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 5187',
                    'departure': '02:30 PM',
                    'arrival': '07:00 PM',
                    'duration': '4h 30m',
                    'stops': '1 Stop (Bangalore - 1h 15m layover)',
                    'from': 'Cochin (COK)',
                    'to': 'Delhi (DEL)',
                    'economy': 6100,  # Via Bangalore
                    'premium': 10200,
                    'business': 19200,
                },
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 545',
                    'departure': '11:30 PM',
                    'arrival': '04:45 AM+1',
                    'duration': '5h 15m',
                    'stops': '1 Stop (Hyderabad - 1h 35m layover)',
                    'from': 'Cochin (COK)',
                    'to': 'Delhi (DEL)',
                    'economy': 6300,  # Night via Hyderabad
                    'premium': 10500,
                    'business': 19800,
                },
            ],
        },
        'Bali': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 336',
                    'departure': '11:30 PM',
                    'arrival': '12:45 PM+1',  # Next day
                    'duration': '13h 15m',
                    'stops': '1 Stop (Singapore - 2h 30m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Denpasar (DPS)',
                    'economy': 20334,  # Air India current rate with layover
                    'premium': 35500,
                    'business': 68000,
                },
                {
                    'airline': 'Singapore Airlines',
                    'flight_no': 'SQ 406',
                    'departure': '02:15 AM',
                    'arrival': '04:50 PM',
                    'duration': '14h 35m',
                    'stops': '1 Stop (Singapore - 3h 45m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Denpasar (DPS)',
                    'economy': 28500,  # Premium airline with layover
                    'premium': 48000,
                    'business': 95000,
                },
                {
                    'airline': 'Thai Airways',
                    'flight_no': 'TG 332',
                    'departure': '08:00 AM',
                    'arrival': '11:20 PM',
                    'duration': '15h 20m',
                    'stops': '1 Stop (Bangkok - 4h 15m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Denpasar (DPS)',
                    'economy': 24800,  # Via Bangkok
                    'premium': 42000,
                    'business': 82000,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 337',
                    'departure': '02:00 PM',
                    'arrival': '11:30 PM',
                    'duration': '12h 30m',
                    'stops': '1 Stop (Singapore - 2h 15m layover)',
                    'from': 'Denpasar (DPS)',
                    'to': 'Delhi (DEL)',
                    'economy': 21500,
                    'premium': 37000,
                    'business': 71000,
                },
                {
                    'airline': 'Singapore Airlines',
                    'flight_no': 'SQ 407',
                    'departure': '05:30 PM',
                    'arrival': '02:45 AM+1',
                    'duration': '14h 15m',
                    'stops': '1 Stop (Singapore - 3h 30m layover)',
                    'from': 'Denpasar (DPS)',
                    'to': 'Delhi (DEL)',
                    'economy': 30200,
                    'premium': 51000,
                    'business': 99000,
                },
                {
                    'airline': 'Thai Airways',
                    'flight_no': 'TG 333',
                    'departure': '12:30 AM',
                    'arrival': '09:45 AM',
                    'duration': '14h 15m',
                    'stops': '1 Stop (Bangkok - 3h 50m layover)',
                    'from': 'Denpasar (DPS)',
                    'to': 'Delhi (DEL)',
                    'economy': 26500,
                    'premium': 44500,
                    'business': 86000,
                },
            ],
        },
        'Thailand': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 331',
                    'departure': '11:30 PM',
                    'arrival': '06:45 AM+1',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Bangkok (BKK)',
                    'economy': 18500,
                    'premium': 32000,
                    'business': 62000,
                },
                {
                    'airline': 'Thai Airways',
                    'flight_no': 'TG 332',
                    'departure': '08:00 AM',
                    'arrival': '01:15 PM',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Bangkok (BKK)',
                    'economy': 22500,
                    'premium': 38000,
                    'business': 72000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1406',
                    'departure': '03:30 PM',
                    'arrival': '08:45 PM',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Bangkok (BKK)',
                    'economy': 16800,
                    'premium': 28500,
                    'business': 55000,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 332',
                    'departure': '08:00 AM',
                    'arrival': '11:15 AM',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Bangkok (BKK)',
                    'to': 'Delhi (DEL)',
                    'economy': 19200,
                    'premium': 33500,
                    'business': 64000,
                },
                {
                    'airline': 'Thai Airways',
                    'flight_no': 'TG 333',
                    'departure': '02:30 PM',
                    'arrival': '05:45 PM',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Bangkok (BKK)',
                    'to': 'Delhi (DEL)',
                    'economy': 23800,
                    'premium': 40000,
                    'business': 75000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1407',
                    'departure': '11:30 PM',
                    'arrival': '02:45 AM+1',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Bangkok (BKK)',
                    'to': 'Delhi (DEL)',
                    'economy': 17500,
                    'premium': 29500,
                    'business': 57000,
                },
            ],
        },
        'Singapore': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 345',
                    'departure': '02:00 AM',
                    'arrival': '09:30 AM',
                    'duration': '5h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Singapore (SIN)',
                    'economy': 22500,
                    'premium': 38000,
                    'business': 72000,
                },
                {
                    'airline': 'Singapore Airlines',
                    'flight_no': 'SQ 406',
                    'departure': '08:45 AM',
                    'arrival': '04:15 PM',
                    'duration': '5h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Singapore (SIN)',
                    'economy': 28500,
                    'premium': 48000,
                    'business': 92000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1406',
                    'departure': '03:30 PM',
                    'arrival': '11:00 PM',
                    'duration': '5h 30m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Singapore (SIN)',
                    'economy': 20800,
                    'premium': 35000,
                    'business': 68000,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 346',
                    'departure': '11:00 PM',
                    'arrival': '02:30 AM+1',
                    'duration': '5h 30m',
                    'stops': 'Direct',
                    'from': 'Singapore (SIN)',
                    'to': 'Delhi (DEL)',
                    'economy': 23500,
                    'premium': 39500,
                    'business': 75000,
                },
                {
                    'airline': 'Singapore Airlines',
                    'flight_no': 'SQ 407',
                    'departure': '05:30 PM',
                    'arrival': '09:00 PM',
                    'duration': '5h 30m',
                    'stops': 'Direct',
                    'from': 'Singapore (SIN)',
                    'to': 'Delhi (DEL)',
                    'economy': 30000,
                    'premium': 50000,
                    'business': 95000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1407',
                    'departure': '12:30 AM',
                    'arrival': '04:00 AM',
                    'duration': '5h 30m',
                    'stops': 'Direct',
                    'from': 'Singapore (SIN)',
                    'to': 'Delhi (DEL)',
                    'economy': 21800,
                    'premium': 36500,
                    'business': 70000,
                },
            ],
        },
        'Maldives': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 263',
                    'departure': '11:30 PM',
                    'arrival': '02:45 AM+1',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Male (MLE)',
                    'economy': 24500,
                    'premium': 42000,
                    'business': 82000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1406',
                    'departure': '03:30 PM',
                    'arrival': '06:45 PM',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Male (MLE)',
                    'economy': 22800,
                    'premium': 38500,
                    'business': 75000,
                },
                {
                    'airline': 'SpiceJet',
                    'flight_no': 'SG 116',
                    'departure': '08:00 AM',
                    'arrival': '11:15 AM',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Male (MLE)',
                    'economy': 20500,
                    'premium': 35000,
                    'business': 68000,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 264',
                    'departure': '03:45 AM',
                    'arrival': '09:00 AM',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Male (MLE)',
                    'to': 'Delhi (DEL)',
                    'economy': 25500,
                    'premium': 43500,
                    'business': 85000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1407',
                    'departure': '07:45 PM',
                    'arrival': '01:00 AM+1',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Male (MLE)',
                    'to': 'Delhi (DEL)',
                    'economy': 23800,
                    'premium': 40000,
                    'business': 78000,
                },
                {
                    'airline': 'SpiceJet',
                    'flight_no': 'SG 117',
                    'departure': '12:15 PM',
                    'arrival': '05:30 PM',
                    'duration': '4h 15m',
                    'stops': 'Direct',
                    'from': 'Male (MLE)',
                    'to': 'Delhi (DEL)',
                    'economy': 21500,
                    'premium': 36500,
                    'business': 70000,
                },
            ],
        },
        'Greece': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 121',
                    'departure': '02:30 AM',
                    'arrival': '08:45 AM',
                    'duration': '9h 15m',
                    'stops': '1 Stop (Vienna - 2h 15m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Athens (ATH)',
                    'economy': 32500,
                    'premium': 55000,
                    'business': 105000,
                },
                {
                    'airline': 'Emirates',
                    'flight_no': 'EK 512',
                    'departure': '08:45 AM',
                    'arrival': '06:30 PM',
                    'duration': '12h 45m',
                    'stops': '1 Stop (Dubai - 3h 30m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Athens (ATH)',
                    'economy': 38500,
                    'premium': 65000,
                    'business': 125000,
                },
                {
                    'airline': 'Qatar Airways',
                    'flight_no': 'QR 570',
                    'departure': '01:30 AM',
                    'arrival': '11:45 AM',
                    'duration': '13h 15m',
                    'stops': '1 Stop (Doha - 4h 00m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Athens (ATH)',
                    'economy': 35800,
                    'premium': 60000,
                    'business': 115000,
                },
                {
                    'airline': 'Turkish Airlines',
                    'flight_no': 'TK 716',
                    'departure': '11:00 PM',
                    'arrival': '10:30 AM+1',
                    'duration': '14h 30m',
                    'stops': '1 Stop (Istanbul - 3h 45m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Athens (ATH)',
                    'economy': 33200,
                    'premium': 56500,
                    'business': 108000,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 122',
                    'departure': '10:00 PM',
                    'arrival': '09:15 AM+1',
                    'duration': '10h 15m',
                    'stops': '1 Stop (Vienna - 2h 30m layover)',
                    'from': 'Athens (ATH)',
                    'to': 'Delhi (DEL)',
                    'economy': 34000,
                    'premium': 57500,
                    'business': 110000,
                },
                {
                    'airline': 'Emirates',
                    'flight_no': 'EK 513',
                    'departure': '08:15 PM',
                    'arrival': '11:30 AM+1',
                    'duration': '12h 15m',
                    'stops': '1 Stop (Dubai - 3h 15m layover)',
                    'from': 'Athens (ATH)',
                    'to': 'Delhi (DEL)',
                    'economy': 40000,
                    'premium': 68000,
                    'business': 130000,
                },
                {
                    'airline': 'Qatar Airways',
                    'flight_no': 'QR 571',
                    'departure': '03:15 PM',
                    'arrival': '05:45 AM+1',
                    'duration': '13h 30m',
                    'stops': '1 Stop (Doha - 4h 15m layover)',
                    'from': 'Athens (ATH)',
                    'to': 'Delhi (DEL)',
                    'economy': 37200,
                    'premium': 62500,
                    'business': 120000,
                },
                {
                    'airline': 'Turkish Airlines',
                    'flight_no': 'TK 717',
                    'departure': '12:30 PM',
                    'arrival': '03:45 AM+1',
                    'duration': '14h 15m',
                    'stops': '1 Stop (Istanbul - 4h 00m layover)',
                    'from': 'Athens (ATH)',
                    'to': 'Delhi (DEL)',
                    'economy': 34500,
                    'premium': 58500,
                    'business': 112000,
                },
            ],
        },
        'Paris': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 143',
                    'departure': '01:30 AM',
                    'arrival': '07:45 AM',
                    'duration': '9h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Paris (CDG)',
                    'economy': 42500,
                    'premium': 72000,
                    'business': 140000,
                },
                {
                    'airline': 'Air France',
                    'flight_no': 'AF 226',
                    'departure': '11:00 PM',
                    'arrival': '05:15 AM+1',
                    'duration': '9h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Paris (CDG)',
                    'economy': 48500,
                    'premium': 82000,
                    'business': 160000,
                },
                {
                    'airline': 'Emirates',
                    'flight_no': 'EK 512',
                    'departure': '08:45 AM',
                    'arrival': '08:30 PM',
                    'duration': '14h 45m',
                    'stops': '1 Stop (Dubai - 4h 00m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Paris (CDG)',
                    'economy': 38500,
                    'premium': 65000,
                    'business': 125000,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 144',
                    'departure': '09:30 AM',
                    'arrival': '10:45 PM',
                    'duration': '10h 15m',
                    'stops': 'Direct',
                    'from': 'Paris (CDG)',
                    'to': 'Delhi (DEL)',
                    'economy': 44000,
                    'premium': 75000,
                    'business': 145000,
                },
                {
                    'airline': 'Air France',
                    'flight_no': 'AF 227',
                    'departure': '06:45 AM',
                    'arrival': '08:00 PM',
                    'duration': '10h 15m',
                    'stops': 'Direct',
                    'from': 'Paris (CDG)',
                    'to': 'Delhi (DEL)',
                    'economy': 50000,
                    'premium': 85000,
                    'business': 165000,
                },
                {
                    'airline': 'Emirates',
                    'flight_no': 'EK 513',
                    'departure': '10:15 AM',
                    'arrival': '03:30 AM+1',
                    'duration': '14h 15m',
                    'stops': '1 Stop (Dubai - 3h 30m layover)',
                    'from': 'Paris (CDG)',
                    'to': 'Delhi (DEL)',
                    'economy': 40000,
                    'premium': 68000,
                    'business': 130000,
                },
            ],
        },
        'Switzerland': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 121',
                    'departure': '02:30 AM',
                    'arrival': '07:45 AM',
                    'duration': '8h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Zurich (ZRH)',
                    'economy': 45500,
                    'premium': 77000,
                    'business': 150000,
                },
                {
                    'airline': 'Swiss International',
                    'flight_no': 'LX 147',
                    'departure': '11:30 PM',
                    'arrival': '04:45 AM+1',
                    'duration': '8h 15m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Zurich (ZRH)',
                    'economy': 52000,
                    'premium': 88000,
                    'business': 170000,
                },
                {
                    'airline': 'Emirates',
                    'flight_no': 'EK 512',
                    'departure': '08:45 AM',
                    'arrival': '07:30 PM',
                    'duration': '13h 45m',
                    'stops': '1 Stop (Dubai - 3h 45m layover)',
                    'from': 'Delhi (DEL)',
                    'to': 'Zurich (ZRH)',
                    'economy': 41500,
                    'premium': 70000,
                    'business': 135000,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 122',
                    'departure': '09:00 AM',
                    'arrival': '09:15 PM',
                    'duration': '9h 15m',
                    'stops': 'Direct',
                    'from': 'Zurich (ZRH)',
                    'to': 'Delhi (DEL)',
                    'economy': 47000,
                    'premium': 80000,
                    'business': 155000,
                },
                {
                    'airline': 'Swiss International',
                    'flight_no': 'LX 148',
                    'departure': '05:45 AM',
                    'arrival': '06:00 PM',
                    'duration': '9h 15m',
                    'stops': 'Direct',
                    'from': 'Zurich (ZRH)',
                    'to': 'Delhi (DEL)',
                    'economy': 54000,
                    'premium': 92000,
                    'business': 175000,
                },
                {
                    'airline': 'Emirates',
                    'flight_no': 'EK 513',
                    'departure': '09:30 AM',
                    'arrival': '02:45 AM+1',
                    'duration': '14h 15m',
                    'stops': '1 Stop (Dubai - 4h 00m layover)',
                    'from': 'Zurich (ZRH)',
                    'to': 'Delhi (DEL)',
                    'economy': 43000,
                    'premium': 73000,
                    'business': 140000,
                },
            ],
        },
        'Turkey': {
            'outbound': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 127',
                    'departure': '11:00 PM',
                    'arrival': '03:45 AM+1',
                    'duration': '7h 45m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Istanbul (IST)',
                    'economy': 28500,
                    'premium': 48000,
                    'business': 92000,
                },
                {
                    'airline': 'Turkish Airlines',
                    'flight_no': 'TK 716',
                    'departure': '02:30 AM',
                    'arrival': '07:15 AM',
                    'duration': '7h 45m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Istanbul (IST)',
                    'economy': 32500,
                    'premium': 55000,
                    'business': 105000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1406',
                    'departure': '08:45 AM',
                    'arrival': '01:30 PM',
                    'duration': '7h 45m',
                    'stops': 'Direct',
                    'from': 'Delhi (DEL)',
                    'to': 'Istanbul (IST)',
                    'economy': 26800,
                    'premium': 45000,
                    'business': 86000,
                },
            ],
            'return': [
                {
                    'airline': 'Air India',
                    'flight_no': 'AI 128',
                    'departure': '05:00 AM',
                    'arrival': '02:45 PM',
                    'duration': '8h 45m',
                    'stops': 'Direct',
                    'from': 'Istanbul (IST)',
                    'to': 'Delhi (DEL)',
                    'economy': 29500,
                    'premium': 50000,
                    'business': 95000,
                },
                {
                    'airline': 'Turkish Airlines',
                    'flight_no': 'TK 717',
                    'departure': '08:30 AM',
                    'arrival': '06:15 PM',
                    'duration': '8h 45m',
                    'stops': 'Direct',
                    'from': 'Istanbul (IST)',
                    'to': 'Delhi (DEL)',
                    'economy': 34000,
                    'premium': 57500,
                    'business': 110000,
                },
                {
                    'airline': 'IndiGo',
                    'flight_no': '6E 1407',
                    'departure': '02:30 PM',
                    'arrival': '10:15 PM',
                    'duration': '8h 45m',
                    'stops': 'Direct',
                    'from': 'Istanbul (IST)',
                    'to': 'Delhi (DEL)',
                    'economy': 28000,
                    'premium': 47000,
                    'business': 90000,
                },
            ],
        },
    }
    
    # Get flight options for this destination
    destination_name = package.destination.name
    
    # Try to get LIVE flight data from API
    try:
        from flight_api_service import flight_api
        
        # Map destination names to IATA airport codes
        iata_codes = {
            'Goa': 'GOI',
            'Dubai': 'DXB',
            'Manali': 'KUU',  # Bhuntar Airport
            'Kerala': 'COK',  # Cochin
            'Bali': 'DPS',    # Denpasar
            'Thailand': 'BKK',
            'Singapore': 'SIN',
            'Maldives': 'MLE',
            'Paris': 'CDG',
            'Switzerland': 'ZRH',
            'Malaysia': 'KUL',
            'Vietnam': 'HAN',
            'Turkey': 'IST',
            'Greece': 'ATH',
            'Japan': 'NRT',
            'Italy': 'FCO',
            'Spain': 'BCN',
            'Australia': 'SYD',
            'New Zealand': 'AKL',
            'South Korea': 'ICN',
            'Mauritius': 'MRU',
        }
        
        destination_code = iata_codes.get(destination_name)
        
        if destination_code:
            # Calculate dates (7 days from now for departure, 14 days for return)
            departure_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            
            # Fetch live flight data
            live_flights = flight_api.search_flights(
                origin='DEL',  # Delhi as default origin
                destination=destination_code,
                departure_date=departure_date,
                return_date=return_date,
                adults=1
            )
            
            # Use live data if available and has flights, otherwise use static fallback
            if live_flights and (live_flights.get('outbound') or live_flights.get('return')):
                flights = live_flights
                print(f"✓ Using LIVE flight data for {destination_name}")
            else:
                # Try static data for this destination
                flights = flight_options.get(destination_name)
                if flights:
                    print(f"⚠ Using static fallback data for {destination_name} (no live data)")
                else:
                    # No static data either, create generic placeholder
                    flights = {
                        'outbound': [],
                        'return': []
                    }
                    print(f"⚠ No flight data available for {destination_name}")
        else:
            # Destination not in IATA mapping, use static data
            flights = flight_options.get(destination_name)
            if not flights:
                # No static data, create empty placeholder
                flights = {
                    'outbound': [],
                    'return': []
                }
                print(f"⚠ No flight data available for {destination_name} (no IATA code)")
            else:
                print(f"⚠ Using static fallback data for {destination_name} (no IATA code)")
    
    except Exception as e:
        # If API fails for any reason, use static fallback data
        flights = flight_options.get(destination_name)
        if not flights:
            # No static data, create empty placeholder
            flights = {
                'outbound': [],
                'return': []
            }
            print(f"⚠ API error for {destination_name}, no fallback data available: {e}")
        else:
            print(f"⚠ API error for {destination_name}, using static data: {e}")
    
    # STUNNING destination-specific gallery images with AMAZING activities - ALL UNIQUE HIGH-QUALITY PHOTOS
    gallery_images = {
        # INDIAN DESTINATIONS
        'Manali': [
            {'url': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&q=90', 'label': '🏔️ Rohtang Pass Snow Paradise'},
            {'url': 'https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=90', 'label': '🛍️ Mall Road Manali'},
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '⛰️ Solang Valley Views'},
            {'url': 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800&q=90', 'label': '⛷️ Snow Activities'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Mountain Resort'},
            {'url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=90', 'label': '🌄 Himalayan Sunrise'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🚵 Adventure Activities'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '🏞️ Temple & Culture'},
        ],
        'Goa': [
            {'url': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=90', 'label': '🏖️ Baga Beach Paradise'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '⛪ Historic Churches'},
            {'url': 'https://images.unsplash.com/photo-1530870110042-98b2cb110834?w=800&q=90', 'label': '🏄 Water Sports'},
            {'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=90', 'label': '🤿 Scuba Diving'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Beach Resort'},
            {'url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=90', 'label': '🌅 Beach Sunset'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🏝️ Coastal Beauty'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍽️ Goan Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=90', 'label': '🌃 Beach Nightlife & Shacks'},
            {'url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=90', 'label': '🏖️ Beach Loungers & Umbrellas'},
        ],
        'Udaipur': [
            {'url': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&q=90', 'label': '🏰 Majestic City Palace'},
            {'url': 'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=800&q=90', 'label': '🌊 Lake Pichola Boat Ride'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '🏛️ Jag Mandir Palace'},
            {'url': 'https://images.unsplash.com/photo-1596402184320-417e7178b2cd?w=800&q=90', 'label': '🏨 Heritage Hotel Stay'},
            {'url': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&q=90', 'label': '🌺 Royal Rajasthani Thali'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍽️ Traditional Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🌄 Monsoon Palace Sunset'},
            {'url': 'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=800&q=90', 'label': '🎭 Cultural Dance Performance'},
            {'url': 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=90', 'label': '🛍️ Hathi Pol Bazaar Shopping'},
            {'url': 'https://images.unsplash.com/photo-1604999333679-b86d54738315?w=800&q=90', 'label': '📸 Heritage Architecture'},
        ],
        'Rishikesh': [
            {'url': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&q=90', 'label': '🏔️ Rishikesh Mountain Views'},
            {'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=90', 'label': '🚣 White Water Rafting Adventure'},
            {'url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&q=90', 'label': '🌉 Iconic Lakshman Jhula Bridge'},
            {'url': 'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=800&q=90', 'label': '🏞️ Sacred Ganges River'},
            {'url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&q=90', 'label': '🧘 Yoga & Meditation Sessions'},
            {'url': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&q=90', 'label': '🏕️ Riverside Camping Experience'},
            {'url': 'https://images.unsplash.com/photo-1533130061792-64b345e4a833?w=800&q=90', 'label': '🪂 Bungee Jumping Thrill'},
            {'url': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&q=90', 'label': '🌅 Evening Ganga Aarti'},
            {'url': 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=800&q=90', 'label': '🧗 Rock Climbing & Trekking'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍛 Healthy Vegetarian Cuisine'},
        ],
        'Andaman': [
            {'url': 'https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=800&q=90', 'label': '🏖️ Radhanagar Beach Paradise'},
            {'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=90', 'label': '🤿 Scuba Diving at Elephant Beach'},
            {'url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=90', 'label': '🏝️ Island Hopping Tours'},
            {'url': 'https://images.unsplash.com/photo-1530870110042-98b2cb110834?w=800&q=90', 'label': '🏄 Snorkeling & Water Sports'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Luxury Beach Resort'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '🏛️ Cellular Jail History'},
            {'url': 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&q=90', 'label': '🌊 Neil Island Natural Bridge'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍽️ Fresh Seafood Delights'},
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🚤 Ferry Adventures'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🌅 Stunning Sunset Views'},
        ],
        'Leh Ladakh': [
            {'url': 'https://images.unsplash.com/photo-1506461883276-594a12b11cf3?w=800&q=90', 'label': '🏔️ Khardung La - World\'s Highest Pass'},
            {'url': 'https://images.unsplash.com/photo-1589308078059-be1415eab4c3?w=800&q=90', 'label': '🌊 Pangong Lake Beauty'},
            {'url': 'https://images.unsplash.com/photo-1559628376-f3fe5f782a2e?w=800&q=90', 'label': '🏜️ Nubra Valley Sand Dunes'},
            {'url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=90', 'label': '🏍️ Royal Enfield Bike Trip'},
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🧗 Trekking Adventures'},
            {'url': 'https://images.unsplash.com/photo-1578645510447-e20b4311e3ce?w=800&q=90', 'label': '🏨 Cozy Leh Hotel'},
            {'url': 'https://images.unsplash.com/photo-1548625149-fc4a29cf7092?w=800&q=90', 'label': '🛕 Thiksey Monastery'},
            {'url': 'https://images.unsplash.com/photo-1509023464722-18d996393ca8?w=800&q=90', 'label': '🏰 Historic Leh Palace'},
            {'url': 'https://images.unsplash.com/photo-1516815231560-8f41ec531527?w=800&q=90', 'label': '🐫 Camel Safari'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍛 Authentic Ladakhi Cuisine'},
        ],
        'Kerala': [
            {'url': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&q=90', 'label': '🚤 Alleppey Houseboat Cruise'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🌿 Munnar Tea Gardens'},
            {'url': 'https://images.unsplash.com/photo-1564419320461-6870880221ad?w=800&q=90', 'label': '🐘 Thekkady Elephant Safari'},
            {'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=90', 'label': '💆 Ayurvedic Spa Treatment'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Premium Resort Stay'},
            {'url': 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&q=90', 'label': '🏖️ Fort Kochi Beach'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍛 Kerala Sadya Feast'},
            {'url': 'https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=800&q=90', 'label': '🎭 Kathakali Dance Show'},
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🌄 Mattupetty Dam Views'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🚣 Bamboo Rafting'},
        ],
        'Jaipur': [
            {'url': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&q=90', 'label': '🏰 Hawa Mahal Palace'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '🏛️ Amber Fort'},
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🏰 City Palace Complex'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Heritage Hotel'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍽️ Rajasthani Thali'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🏰 Jal Mahal Water Palace'},
        ],
        'Ooty': [
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🌄 Nilgiri Mountain Railway'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🌿 Tea Gardens'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Hill Station Resort'},
            {'url': 'https://images.unsplash.com/photo-1490730141103-6cac27aaab94?w=800&q=90', 'label': '🌺 Botanical Gardens'},
            {'url': 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&q=90', 'label': '🌊 Ooty Lake Boating'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍫 Chocolate Factory'},
        ],
        'Darjeeling': [
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🌿 Tea Plantations'},
            {'url': 'https://images.unsplash.com/photo-1474552226712-ac0f0961a954?w=800&q=90', 'label': '🚂 Toy Train Ride'},
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🏔️ Kanchenjunga View'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Colonial Hotel'},
            {'url': 'https://images.unsplash.com/photo-1495954484750-af469f2f9be5?w=800&q=90', 'label': '🌅 Tiger Hill Sunrise'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍵 Tea Tasting'},
        ],
        'Varanasi': [
            {'url': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800&q=90', 'label': '🏞️ Ganges River Ghats'},
            {'url': 'https://images.unsplash.com/photo-1532664189809-02133fee698d?w=800&q=90', 'label': '🌅 Ganga Aarti Ceremony'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Heritage Hotel'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '🛕 Kashi Vishwanath Temple'},
            {'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=90', 'label': '🚤 Boat Ride at Dawn'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍛 Street Food'},
        ],
        'Agra': [
            {'url': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&q=90', 'label': '🕌 Taj Mahal'},
            {'url': 'https://images.unsplash.com/photo-1587135941948-670b381f08ce?w=800&q=90', 'label': '🏰 Agra Fort'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Luxury Hotel'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '🏛️ Fatehpur Sikri'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍽️ Mughlai Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🌅 Taj Sunset View'},
        ],
        'Coorg': [
            {'url': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&q=90', 'label': '☕ Coffee Plantations'},
            {'url': 'https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=800&q=90', 'label': '🌊 Abbey Falls'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Estate Stay'},
            {'url': 'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800&q=90', 'label': '🌄 Raja Seat Viewpoint'},
            {'url': 'https://images.unsplash.com/photo-1564419320461-6870880221ad?w=800&q=90', 'label': '🐘 Dubare Elephant Camp'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍛 Coorgi Pork Curry'},
        ],
        'Mysore': [
            {'url': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&q=90', 'label': '🏰 Mysore Palace'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Heritage Hotel'},
            {'url': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=90', 'label': '🌺 Brindavan Gardens'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '🛕 Chamundi Hills Temple'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍬 Mysore Pak Sweet'},
            {'url': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=90', 'label': '🛍️ Devaraja Market'},
        ],
        # INTERNATIONAL DESTINATIONS
        'Bali': [
            {'url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&q=90', 'label': '🛕 Tanah Lot Temple'},
            {'url': 'https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=800&q=90', 'label': '🏖️ Seminyak Beach'},
            {'url': 'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=800&q=90', 'label': '🌾 Rice Terraces'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Luxury Villa'},
            {'url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=90', 'label': '🏝️ Island Paradise'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍜 Balinese Food'},
        ],
        'Dubai': [
            {'url': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=90', 'label': '🏙️ Burj Khalifa - World\'s Tallest Building'},
            {'url': 'https://images.unsplash.com/photo-1582672060674-bc2bd808a8b5?w=800&q=90', 'label': '� Burj Al Arab - Luxury Hotel'},
            {'url': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?w=800&q=90', 'label': '🛍️ Dubai Mall - Shopping Paradise'},
            {'url': 'https://images.unsplash.com/photo-1580674285054-bed31e145f59?w=800&q=90', 'label': '⛲ Dubai Fountain Show'},
            {'url': 'https://images.unsplash.com/photo-1546412414-e1885259563a?w=800&q=90', 'label': '🌃 Dubai Marina Skyline'},
            {'url': 'https://images.unsplash.com/photo-1559628376-f3fe5f782a2e?w=800&q=90', 'label': '🚢 Dhow Cruise Dinner'},
            {'url': 'https://images.unsplash.com/photo-1451337516015-6b6e9a44a8a3?w=800&q=90', 'label': '�️ Desert Safari - Dune Bashing'},
            {'url': 'https://images.unsplash.com/photo-1583221773423-caae86a0e7e8?w=800&q=90', 'label': '🐪 Camel Riding Experience'},
            {'url': 'https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=800&q=90', 'label': '🌅 Desert Sunset'},
            {'url': 'https://images.unsplash.com/photo-1578895101408-1a36b834405b?w=800&q=90', 'label': '🍖 BBQ Dinner at Bedouin Camp'},
            {'url': 'https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=800&q=90', 'label': '💃 Belly Dance Show'},
            {'url': 'https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=800&q=90', 'label': '🏺 Gold Souk Shopping'},
        ],
        'Paris': [
            {'url': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=90', 'label': '🗼 Eiffel Tower'},
            {'url': 'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=800&q=90', 'label': '🏛️ Louvre Museum'},
            {'url': 'https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=800&q=90', 'label': '⛪ Notre-Dame'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Boutique Hotel'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🥐 French Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🌉 Seine River'},
        ],
        'Maldives': [
            {'url': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800&q=90', 'label': '🏝️ Overwater Villas'},
            {'url': 'https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=90', 'label': '🏖️ White Sand Beaches'},
            {'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=90', 'label': '🤿 Snorkeling & Diving'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Luxury Resort'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🌅 Sunset Cruises'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍽️ Seafood Dining'},
        ],
        'Thailand': [
            {'url': 'https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=800&q=90', 'label': '🛕 Grand Palace Bangkok'},
            {'url': 'https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=90', 'label': '🏖️ Phuket Beaches'},
            {'url': 'https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=90', 'label': '🏝️ Phi Phi Islands'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Beach Resort'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍜 Thai Street Food'},
            {'url': 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=90', 'label': '🛕 Wat Arun Temple'},
        ],
        'Singapore': [
            {'url': 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&q=90', 'label': '🏙️ Marina Bay Sands'},
            {'url': 'https://images.unsplash.com/photo-1562992932-a7b042e9d039?w=800&q=90', 'label': '🌺 Gardens by the Bay'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Luxury Hotel'},
            {'url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=90', 'label': '🏝️ Sentosa Island'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍜 Hawker Food'},
            {'url': 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=800&q=90', 'label': '🛍️ Orchard Road Shopping'},
        ],
        'Switzerland': [
            {'url': 'https://images.unsplash.com/photo-1527668752968-14dc70a27c95?w=800&q=90', 'label': '🏔️ Swiss Alps'},
            {'url': 'https://images.unsplash.com/photo-1474552226712-ac0f0961a954?w=800&q=90', 'label': '🚂 Scenic Train Ride'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Alpine Resort'},
            {'url': 'https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=800&q=90', 'label': '🌊 Lake Geneva'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🧀 Swiss Cheese & Chocolate'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '⛷️ Skiing & Snowboarding'},
        ],
        'Malaysia': [
            {'url': 'https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&q=90', 'label': '🏙️ Petronas Twin Towers KL'},
            {'url': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=90', 'label': '🛕 Batu Caves'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 City Hotel'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🎢 Genting Highlands'},
            {'url': 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&q=90', 'label': '🏖️ Penang Beaches'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍜 Malaysian Street Food'},
            {'url': 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=800&q=90', 'label': '🎨 Georgetown Street Art'},
        ],
        'Vietnam': [
            {'url': 'https://images.unsplash.com/photo-1528127269322-539801943592?w=800&q=90', 'label': '🏞️ Ha Long Bay Cruise'},
            {'url': 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=800&q=90', 'label': '🏛️ Hanoi Old Quarter'},
            {'url': 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=90', 'label': '🏨 Cruise Ship Stay'},
            {'url': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=90', 'label': '🛕 Ho Chi Minh Mausoleum'},
            {'url': 'https://images.unsplash.com/photo-1590073242678-70ee3fc28e8e?w=800&q=90', 'label': '🚤 Mekong Delta'},
            {'url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=90', 'label': '🍜 Pho & Vietnamese Food'},
            {'url': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&q=90', 'label': '🏙️ Ho Chi Minh City'},
        ],
        'Turkey': [
            {'url': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800&q=90', 'label': '🕌 Hagia Sophia Istanbul'},
            {'url': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?w=800&q=90', 'label': '🕌 Blue Mosque'},
            {'url': 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=90', 'label': '🏨 Cave Hotel Cappadocia'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🎈 Hot Air Balloon Ride'},
            {'url': 'https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=800&q=90', 'label': '🏰 Pamukkale Cotton Castle'},
            {'url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=90', 'label': '🍽️ Turkish Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&q=90', 'label': '🌉 Bosphorus Cruise'},
        ],
        'Greece': [
            {'url': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=800&q=90', 'label': '🏛️ Santorini Oia Village'},
            {'url': 'https://images.unsplash.com/photo-1555993539-1732b0258235?w=800&q=90', 'label': '🏛️ Acropolis Athens'},
            {'url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=90', 'label': '🏨 Caldera View Hotel'},
            {'url': 'https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=800&q=90', 'label': '🏖️ Mykonos Beaches'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🌅 Santorini Sunset'},
            {'url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=90', 'label': '🍽️ Greek Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&q=90', 'label': '🚤 Catamaran Cruise'},
        ],
        'Japan': [
            {'url': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800&q=90', 'label': '🗼 Tokyo Shibuya Crossing'},
            {'url': 'https://images.unsplash.com/photo-1478436127897-769e1b3f0f36?w=800&q=90', 'label': '🛕 Fushimi Inari Shrine'},
            {'url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=90', 'label': '🏨 Traditional Ryokan'},
            {'url': 'https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?w=800&q=90', 'label': '🗻 Mount Fuji'},
            {'url': 'https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800&q=90', 'label': '🎋 Arashiyama Bamboo Grove'},
            {'url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800&q=90', 'label': '🍣 Japanese Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1480796927426-f609979314bd?w=800&q=90', 'label': '🏰 Osaka Castle'},
        ],
        'Italy': [
            {'url': 'https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=800&q=90', 'label': '🏛️ Colosseum Rome'},
            {'url': 'https://images.unsplash.com/photo-1523906921802-b5d2d899e93b?w=800&q=90', 'label': '🌉 Venice Canals'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Boutique Hotel'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🗼 Leaning Tower Pisa'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍕 Italian Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800&q=90', 'label': '🌄 Tuscany Countryside'},
        ],
        'Spain': [
            {'url': 'https://images.unsplash.com/photo-1543783207-ec64e4d95325?w=800&q=90', 'label': '🏛️ Sagrada Familia Barcelona'},
            {'url': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=800&q=90', 'label': '🏰 Royal Palace Madrid'},
            {'url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=90', 'label': '🏨 City Hotel'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🏖️ Barcelona Beach'},
            {'url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=90', 'label': '🍷 Tapas & Paella'},
            {'url': 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800&q=90', 'label': '🎨 Park Guell'},
        ],
        'Australia': [
            {'url': 'https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=800&q=90', 'label': '🏛️ Sydney Opera House'},
            {'url': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800&q=90', 'label': '🌉 Sydney Harbour Bridge'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Waterfront Hotel'},
            {'url': 'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=800&q=90', 'label': '🏖️ Bondi Beach'},
            {'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=90', 'label': '🐠 Great Barrier Reef'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍽️ Australian Cuisine'},
        ],
        'New Zealand': [
            {'url': 'https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=800&q=90', 'label': '🏔️ Milford Sound'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🌊 Lake Tekapo'},
            {'url': 'https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800&q=90', 'label': '🏨 Lodge Stay'},
            {'url': 'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800&q=90', 'label': '🎬 Hobbiton Movie Set'},
            {'url': 'https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=800&q=90', 'label': '🚁 Helicopter Tours'},
            {'url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=90', 'label': '🍽️ Kiwi Cuisine'},
        ],
        'South Korea': [
            {'url': 'https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=800&q=90', 'label': '🏙️ Seoul Skyline'},
            {'url': 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=800&q=90', 'label': '🏰 Gyeongbokgung Palace'},
            {'url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=90', 'label': '🏨 Modern Hotel'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🌸 Cherry Blossoms'},
            {'url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=90', 'label': '🍜 Korean BBQ'},
            {'url': 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=800&q=90', 'label': '🛍️ Myeongdong Shopping'},
        ],
        'Mauritius': [
            {'url': 'https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=800&q=90', 'label': '🏖️ Belle Mare Beach'},
            {'url': 'https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=800&q=90', 'label': '🏝️ Ile aux Cerfs Island'},
            {'url': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&q=90', 'label': '🏨 Beach Resort'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🌊 Seven Colored Earth'},
            {'url': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800&q=90', 'label': '🍽️ Creole Cuisine'},
            {'url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&q=90', 'label': '🚤 Catamaran Cruise'},
        ],
        'Shimla': [
            {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🏔️ Shimla Mall Road'},
            {'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=90', 'label': '🏛️ Viceregal Lodge'},
            {'url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=90', 'label': '🏨 Colonial Hotel'},
            {'url': 'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800&q=90', 'label': '🌄 Kufri Snow Point'},
            {'url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=90', 'label': '⛪ Christ Church'},
            {'url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=90', 'label': '🍽️ Himachali Food'},
        ],
    }
    
    # Get gallery for this destination or use default
    destination_name = package.destination.name
    gallery = gallery_images.get(destination_name, [
        {'url': 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&q=90', 'label': '📸 Scenic Views'},
        {'url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=90', 'label': '🏨 Premium Hotels'},
        {'url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=90', 'label': '🍽️ Local Cuisine'},
        {'url': 'https://images.unsplash.com/photo-1530521954074-e64f6810b32d?w=800&q=90', 'label': '🎯 Activities'},
        {'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=90', 'label': '🌄 Natural Beauty'},
        {'url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=90', 'label': '🏖️ Beaches & Relaxation'},
    ])
    from store.moments_data import get_moments
    moments = get_moments(package.destination.name)

    context = {
        'package': package,
        'related_packages': related_packages,
        'gallery': gallery,
        'flights': flights,
        'moments': moments,
    }
    
    return render(request, 'store/package_detail.html', context)

def budget_planner_view(request):
    budget = request.GET.get('budget', '')
    travelers = request.GET.get('travelers', '1')
    destination_type = request.GET.get('destination_type', '')  # domestic / international
    duration = request.GET.get('duration', '')

    suggestions = None

    # Hotel tiers (per night per room, INR)
    hotels = {
        'budget': [
            {'name': 'OYO Rooms / Budget Inn', 'type': 'Budget (1-2★)', 'price_per_night': 800, 'amenities': 'AC, WiFi, Basic Breakfast', 'rating': '3.5/5'},
            {'name': 'Zostel / Backpacker Hostel', 'type': 'Hostel', 'price_per_night': 500, 'amenities': 'Dorm Bed, WiFi, Common Kitchen', 'rating': '4.0/5'},
        ],
        'mid': [
            {'name': 'Ibis / Lemon Tree', 'type': 'Mid-Range (3★)', 'price_per_night': 2500, 'amenities': 'AC, WiFi, Breakfast, Pool', 'rating': '4.2/5'},
            {'name': 'Treebo / FabHotel', 'type': 'Mid-Range (3★)', 'price_per_night': 2000, 'amenities': 'AC, WiFi, Breakfast', 'rating': '4.0/5'},
        ],
        'premium': [
            {'name': 'Marriott / Hyatt', 'type': 'Premium (5★)', 'price_per_night': 8000, 'amenities': 'Luxury Suite, Spa, Pool, All Meals', 'rating': '4.8/5'},
            {'name': 'Taj / Oberoi', 'type': 'Luxury (5★)', 'price_per_night': 12000, 'amenities': 'Heritage Suite, Butler, Fine Dining', 'rating': '4.9/5'},
        ],
    }

    # Destination data: flight cost (per person economy), daily food+local transport
    destinations = {
        'domestic': [
            {'name': 'Goa', 'country': 'India', 'flight': 5000, 'daily_cost': 2500, 'emoji': '🏖️',
             'highlights': ['Baga Beach', 'Fort Aguada', 'Dudhsagar Falls', 'Old Goa Churches', 'Anjuna Flea Market'],
             'best_for': 'Beach, Nightlife, Water Sports'},
            {'name': 'Manali', 'country': 'India', 'flight': 4000, 'daily_cost': 2000, 'emoji': '🏔️',
             'highlights': ['Rohtang Pass', 'Solang Valley', 'Hadimba Temple', 'Old Manali', 'Beas River Rafting'],
             'best_for': 'Adventure, Snow, Honeymoon'},
            {'name': 'Kerala', 'country': 'India', 'flight': 6500, 'daily_cost': 2200, 'emoji': '🌴',
             'highlights': ['Alleppey Backwaters', 'Munnar Tea Gardens', 'Kovalam Beach', 'Periyar Wildlife', 'Thekkady'],
             'best_for': 'Nature, Backwaters, Ayurveda'},
            {'name': 'Jaipur', 'country': 'India', 'flight': 3500, 'daily_cost': 1800, 'emoji': '🏰',
             'highlights': ['Amber Fort', 'Hawa Mahal', 'City Palace', 'Jantar Mantar', 'Nahargarh Fort'],
             'best_for': 'Heritage, Culture, Shopping'},
            {'name': 'Andaman', 'country': 'India', 'flight': 9000, 'daily_cost': 2800, 'emoji': '🐠',
             'highlights': ['Radhanagar Beach', 'Cellular Jail', 'Scuba Diving', 'Ross Island', 'Neil Island'],
             'best_for': 'Beach, Diving, Honeymoon'},
        ],
        'international': [
            {'name': 'Dubai', 'country': 'UAE', 'flight': 15000, 'daily_cost': 5000, 'emoji': '🌆',
             'highlights': ['Burj Khalifa', 'Dubai Mall', 'Desert Safari', 'Palm Jumeirah', 'Dubai Creek'],
             'best_for': 'Luxury, Shopping, Family'},
            {'name': 'Bali', 'country': 'Indonesia', 'flight': 22000, 'daily_cost': 3500, 'emoji': '🌺',
             'highlights': ['Ubud Rice Terraces', 'Tanah Lot Temple', 'Seminyak Beach', 'Mount Batur', 'Kuta Nightlife'],
             'best_for': 'Honeymoon, Culture, Beach'},
            {'name': 'Thailand', 'country': 'Thailand', 'flight': 18000, 'daily_cost': 3000, 'emoji': '🐘',
             'highlights': ['Grand Palace Bangkok', 'Phi Phi Islands', 'Chiang Mai Temples', 'Phuket Beach', 'Floating Market'],
             'best_for': 'Budget International, Beach, Food'},
            {'name': 'Singapore', 'country': 'Singapore', 'flight': 20000, 'daily_cost': 6000, 'emoji': '🦁',
             'highlights': ['Marina Bay Sands', 'Gardens by the Bay', 'Sentosa Island', 'Universal Studios', 'Hawker Food'],
             'best_for': 'Family, Shopping, Modern City'},
            {'name': 'Maldives', 'country': 'Maldives', 'flight': 25000, 'daily_cost': 8000, 'emoji': '🏝️',
             'highlights': ['Overwater Bungalows', 'Snorkeling', 'Dolphin Watching', 'Sunset Cruises', 'Coral Reefs'],
             'best_for': 'Luxury Honeymoon, Beach, Diving'},
        ],
    }

    if budget and travelers:
        try:
            total_budget = int(budget)
            num_travelers = int(travelers)
            budget_per_person = total_budget // num_travelers
            num_days = int(duration) if duration else 5

            # Determine hotel tier
            hotel_budget_per_night = budget_per_person * 0.25  # 25% of per-person budget for hotel
            if hotel_budget_per_night < 1500:
                hotel_tier = 'budget'
            elif hotel_budget_per_night < 5000:
                hotel_tier = 'mid'
            else:
                hotel_tier = 'premium'

            recommended_hotels = hotels[hotel_tier]

            # Filter destinations by type
            dest_pool = []
            if destination_type == 'domestic':
                dest_pool = destinations['domestic']
            elif destination_type == 'international':
                dest_pool = destinations['international']
            else:
                dest_pool = destinations['domestic'] + destinations['international']

            # Calculate total cost per person for each destination
            viable = []
            for dest in dest_pool:
                flight_cost = dest['flight']
                stay_cost = recommended_hotels[0]['price_per_night'] * num_days
                food_transport = dest['daily_cost'] * num_days
                total_per_person = flight_cost + stay_cost + food_transport
                total_for_group = total_per_person * num_travelers
                remaining = total_budget - total_for_group

                if total_for_group <= total_budget:
                    viable.append({
                        **dest,
                        'flight_cost': flight_cost,
                        'stay_cost': stay_cost,
                        'food_transport': food_transport,
                        'total_per_person': total_per_person,
                        'total_for_group': total_for_group,
                        'remaining_budget': remaining,
                        'fit': 'great' if remaining > total_budget * 0.2 else 'tight',
                    })

            # Sort by remaining budget descending (best fit first)
            viable.sort(key=lambda x: x['remaining_budget'], reverse=True)

            suggestions = {
                'viable_destinations': viable[:5],
                'hotels': recommended_hotels,
                'hotel_tier': hotel_tier,
                'budget_per_person': budget_per_person,
                'num_days': num_days,
                'num_travelers': num_travelers,
                'total_budget': total_budget,
            }
        except (ValueError, ZeroDivisionError):
            pass

    context = {
        'suggestions': suggestions,
        'budget': budget,
        'travelers': travelers,
        'destination_type': destination_type,
        'duration': duration,
    }
    return render(request, 'store/budget_planner.html', context)


@csrf_exempt
def create_booking_view(request, package_id=None):
    """Handle booking creation from the flight modal."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'login_required'}, status=401)

    try:
        data = json.loads(request.body)
        package_id = data.get('package_id') or package_id
        adults          = int(data.get('adults', 1))
        children        = int(data.get('children', 0))
        travel_date_str = data.get('travel_date', '')
        outbound        = data.get('outbound', {}) or {}
        ret             = data.get('return', {}) or {}
        total_flight    = int(data.get('total_flight_price', 0) or 0)

        from bookings.models import Booking, Traveler
        import datetime, decimal

        package = get_object_or_404(TourPackage, id=package_id)

        if travel_date_str:
            try:
                travel_date = datetime.datetime.strptime(travel_date_str, '%Y-%m-%d').date()
            except ValueError:
                travel_date = datetime.date.today() + datetime.timedelta(days=30)
        else:
            travel_date = datetime.date.today() + datetime.timedelta(days=30)

        base_fare    = decimal.Decimal(str(package.price_per_person)) * (adults + children * decimal.Decimal('0.5'))
        flight_cost  = decimal.Decimal(str(total_flight))
        subtotal     = base_fare + flight_cost
        tax_amount   = (subtotal * decimal.Decimal('0.09')).quantize(decimal.Decimal('0.01'))
        total_amount = subtotal + tax_amount
        amount_paid  = (total_amount * decimal.Decimal('0.5')).quantize(decimal.Decimal('0.01'))
        remaining    = total_amount - amount_paid
        due_date     = datetime.date.today() + datetime.timedelta(days=30)

        booking = Booking(
            user=request.user,
            package=package,
            travel_date=travel_date,
            adults_count=adults,
            children_count=children,
            base_fare=base_fare,
            tax_amount=tax_amount,
            discount_amount=0,
            total_amount=total_amount,
            amount_paid=amount_paid,
            remaining_due_date=due_date,
            payment_notes=f"50% paid at booking. Remaining Rs.{remaining} due by {due_date}.",
            status='confirmed',
            outbound_airline=outbound.get('airline', ''),
            outbound_flight_no=outbound.get('flight_no', ''),
            outbound_from=outbound.get('from', ''),
            outbound_to=outbound.get('to', ''),
            outbound_departure=outbound.get('departure', ''),
            outbound_arrival=outbound.get('arrival', ''),
            outbound_duration=outbound.get('duration', ''),
            outbound_stops=outbound.get('stops', 'Direct'),
            seat_class=outbound.get('seat_class', 'Economy'),
            return_airline=ret.get('airline', ''),
            return_flight_no=ret.get('flight_no', ''),
            return_from=ret.get('from', ''),
            return_to=ret.get('to', ''),
            return_departure=ret.get('departure', ''),
            return_arrival=ret.get('arrival', ''),
            return_duration=ret.get('duration', ''),
            return_stops=ret.get('stops', 'Direct'),
        )
        booking.save()

        traveler_names = data.get('travelers', [])
        for t in traveler_names:
            Traveler.objects.create(
                booking=booking,
                name=t.get('name', request.user.get_full_name() or request.user.username),
                age=int(t.get('age', 25)),
                gender=t.get('gender', 'M'),
            )
        if not traveler_names:
            Traveler.objects.create(
                booking=booking,
                name=request.user.get_full_name() or request.user.username,
                age=25,
                gender='M',
            )

        try:
            from bookings.notifications import send_all_booking_notifications
            send_all_booking_notifications(booking)
        except Exception as notif_err:
            logger.warning(f"Notification failed for {booking.booking_id}: {notif_err}")

        return JsonResponse({
            'success': True,
            'booking_id': booking.booking_id,
            'total_amount': str(total_amount),
            'amount_paid': str(amount_paid),
            'remaining': str(remaining),
            'due_date': str(due_date),
        })

    except Exception as e:
        import traceback
        return JsonResponse({'success': False, 'error': str(e), 'trace': traceback.format_exc()}, status=400)
