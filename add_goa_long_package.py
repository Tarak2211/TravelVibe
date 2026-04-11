"""
Add a longer Goa package (8-14 days)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from store.models import Destination, TourPackage
from datetime import date, timedelta

def add_goa_long_package():
    print("Adding longer Goa package...")
    
    # Get or create Goa destination
    goa, created = Destination.objects.get_or_create(
        name="Goa",
        defaults={
            "country": "India",
            "description": "Beautiful beaches and vibrant nightlife",
            "is_trending": True
        }
    )
    
    if created:
        print(f"✓ Created destination: Goa")
    else:
        print(f"✓ Found existing destination: Goa")
    
    # Add 10-day Goa package
    package_data = {
        "title": "Goa Complete Experience",
        "destination": goa,
        "category": "family",
        "duration": "8-14",
        "price": 32999,
        "price_per_person": 32999,
        "price_per_couple": 62999,
        "price_per_group": 119999,
        "emi_per_month": 5500,
        "emi_available": True,
        "description": "Extended 10-day Goa vacation covering North & South Goa beaches, water sports, nightlife, and heritage sites",
        "inclusions": "4-star hotel accommodation, Daily breakfast and dinner, Airport transfers, All sightseeing tours, Water sports package, Cruise party tickets",
        "exclusions": "Airfare, Lunch, Personal expenses, Travel insurance, Additional activities",
        "itinerary": """Day 1: Arrival in Goa
- Flight: AI 502 Delhi to Goa (06:00 AM - 08:30 AM) - ₹4,500
- Check-in at hotel by 10:00 AM
- Relax at Calangute Beach
- Evening: Baga Beach sunset and shopping
- Overnight at hotel

Day 2: North Goa Beaches
- 09:00 AM: Fort Aguada visit
- 11:00 AM: Chapora Fort (Dil Chahta Hai fort)
- 01:00 PM: Lunch at beach shack
- 03:00 PM: Anjuna Beach and flea market
- 06:00 PM: Vagator Beach sunset
- Overnight at hotel

Day 3: Water Sports Extravaganza
- 09:00 AM: Parasailing (₹800), Jet Ski (₹600)
- 11:00 AM: Banana Boat Ride (₹400)
- 02:00 PM: Scuba Diving (₹2,500)
- Evening: Candolim Beach relaxation
- Night: Tito's Lane nightlife
- Overnight at hotel

Day 4: Heritage & Culture
- 09:00 AM: Basilica of Bom Jesus
- 11:00 AM: Se Cathedral
- 01:00 PM: Lunch at Panjim
- 03:00 PM: Fontainhas Latin Quarter walk
- 05:00 PM: Miramar Beach
- Overnight at hotel

Day 5: South Goa Exploration
- 08:00 AM: Drive to South Goa
- 10:00 AM: Palolem Beach
- 12:00 PM: Lunch at beach restaurant
- 02:00 PM: Cabo de Rama Fort
- 04:00 PM: Agonda Beach
- 06:00 PM: Return to hotel
- Overnight at hotel

Day 6: Island & Backwaters
- 08:00 AM: Boat to Divar Island
- 10:00 AM: Village cycling tour
- 12:00 PM: Traditional Goan lunch
- 02:00 PM: Backwater cruise
- 05:00 PM: Sunset at Dona Paula
- Overnight at hotel

Day 7: Adventure Day
- 09:00 AM: Dudhsagar Waterfalls trek
- 12:00 PM: Spice plantation tour
- 02:00 PM: Traditional Goan lunch
- 04:00 PM: Elephant bath experience
- 07:00 PM: Return to hotel
- Overnight at hotel

Day 8: Casino & Cruise
- Morning: Leisure at hotel/beach
- 12:00 PM: Lunch at hotel
- 03:00 PM: Shopping at Mapusa Market
- 06:00 PM: Sunset cruise with dinner
- 09:00 PM: Casino cruise (₹2,000)
- Overnight at hotel

Day 9: Beach Hopping
- 09:00 AM: Morjim Beach (Turtle beach)
- 11:00 AM: Ashwem Beach
- 01:00 PM: Lunch at beach shack
- 03:00 PM: Arambol Beach
- 05:00 PM: Keri Beach sunset
- Overnight at hotel

Day 10: Departure
- Morning: Last beach visit
- 11:00 AM: Check-out
- 12:00 PM: Lunch at restaurant
- 02:00 PM: Airport transfer
- Flight: AI 503 Goa to Delhi (04:00 PM - 06:30 PM) - ₹4,800""",
        "is_featured": True,
        "available_from": date.today(),
        "available_to": date.today() + timedelta(days=365),
        "popularity_score": 95
    }
    
    pkg, created = TourPackage.objects.get_or_create(
        title=package_data["title"],
        defaults=package_data
    )
    
    if created:
        print(f"✓ Created package: {pkg.title}")
    else:
        # Update existing package
        for key, value in package_data.items():
            setattr(pkg, key, value)
        pkg.save()
        print(f"✓ Updated package: {pkg.title}")
    
    print("\n✅ Goa long package added successfully!")
    print(f"Package: {pkg.title}")
    print(f"Duration: {pkg.get_duration_display()}")
    print(f"Price: ₹{pkg.price}")

if __name__ == "__main__":
    add_goa_long_package()
