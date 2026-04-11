"""
Populate sample data for TravelVibe
Run after migrations: python populate_sample_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from store.models import Destination, TourPackage, Banner, Testimonial
from datetime import date, timedelta

def populate_data():
    print("Creating sample destinations...")
    
    destinations_data = [
        {"name": "Goa", "country": "India", "description": "Beautiful beaches and vibrant nightlife", "is_trending": True},
        {"name": "Bali", "country": "Indonesia", "description": "Tropical paradise with stunning temples", "is_trending": True},
        {"name": "Manali", "country": "India", "description": "Scenic mountain town in the Himalayas", "is_trending": True},
        {"name": "Paris", "country": "France", "description": "City of lights and romance", "is_trending": True},
        {"name": "Dubai", "country": "UAE", "description": "Modern luxury and desert adventures", "is_trending": True},
        {"name": "Maldives", "country": "Maldives", "description": "Crystal clear waters and luxury resorts", "is_trending": True},
        {"name": "Kerala", "country": "India", "description": "God's own country with backwaters", "is_trending": True},
        {"name": "Jaipur", "country": "India", "description": "Pink city with royal heritage", "is_trending": True},
        {"name": "Thailand", "country": "Thailand", "description": "Land of smiles and beaches", "is_trending": True},
        {"name": "Switzerland", "country": "Switzerland", "description": "Alpine paradise with snow peaks", "is_trending": True},
        {"name": "Singapore", "country": "Singapore", "description": "Modern city with gardens", "is_trending": True},
        {"name": "Shimla", "country": "India", "description": "Queen of hills", "is_trending": True},
    ]
    
    destinations = []
    for dest_data in destinations_data:
        dest, created = Destination.objects.get_or_create(
            name=dest_data["name"],
            defaults=dest_data
        )
        destinations.append(dest)
        if created:
            print(f"✓ Created destination: {dest.name}")
    
    print("\nCreating sample tour packages...")
    
    packages_data = [
        {
            "title": "Goa Beach Paradise", 
            "destination": destinations[0], 
            "category": "family", 
            "duration": "4-7", 
            "price": 18999,
            "price_per_person": 18999,
            "price_per_couple": 35999,
            "price_per_group": 67999,
            "emi_per_month": 3167,
            "description": "Enjoy sun, sand, and sea in Goa's best beaches with water sports and nightlife",
            "inclusions": "4-star hotel accommodation, Daily breakfast and dinner, Airport transfers, Sightseeing tours, Water sports activities",
            "exclusions": "Airfare, Lunch, Personal expenses, Travel insurance, Monument entry fees",
            "itinerary": """Day 1: Arrival in Goa
- Flight: AI 502 Delhi to Goa (06:00 AM - 08:30 AM) - ₹4,500
- Check-in at hotel by 10:00 AM
- Relax at Calangute Beach
- Evening: Baga Beach sunset and shopping
- Overnight at hotel

Day 2: North Goa Sightseeing
- 09:00 AM: Fort Aguada visit
- 11:00 AM: Chapora Fort (Dil Chahta Hai fort)
- 01:00 PM: Lunch at beach shack
- 03:00 PM: Anjuna Beach and flea market
- 06:00 PM: Vagator Beach sunset
- Overnight at hotel

Day 3: Water Sports & Beach Activities
- 09:00 AM: Parasailing (₹800), Jet Ski (₹600)
- 11:00 AM: Banana Boat Ride (₹400)
- 02:00 PM: Scuba Diving (₹2,500)
- Evening: Candolim Beach relaxation
- Night: Casino cruise (optional - ₹2,000)
- Overnight at hotel

Day 4: South Goa & Departure
- 08:00 AM: Palolem Beach visit
- 10:00 AM: Cabo de Rama Fort
- 12:00 PM: Lunch at beach restaurant
- 02:00 PM: Check-out and airport transfer
- Flight: AI 503 Goa to Delhi (04:00 PM - 06:30 PM) - ₹4,800"""
        },
        {
            "title": "Bali Honeymoon Special", 
            "destination": destinations[1], 
            "category": "honeymoon", 
            "duration": "8-14", 
            "price": 114567,
            "price_per_person": 114567,
            "price_per_couple": 229134,
            "price_per_group": 458268,
            "emi_per_month": 30198,
            "description": "Romantic 7-day getaway in tropical Bali with private villa, spa, and island tours",
            "inclusions": "5-star private villa with pool, Daily breakfast, Airport transfers, Romantic candlelight dinner, Couple spa session, All sightseeing tours",
            "exclusions": "International flights, Visa fees (₹3,500), Lunch and dinner (except mentioned), Travel insurance, Personal expenses",
            "itinerary": """Day 1: Arrival in Bali
- Flight: SG 511 Delhi to Bali (11:00 PM - 09:00 AM+1) - ₹35,000
- Private transfer to Ubud villa
- Check-in at 02:00 PM
- Welcome drink and villa tour
- Evening: Romantic dinner at villa
- Overnight at private villa

Day 2: Ubud Cultural Tour
- 09:00 AM: Tegalalang Rice Terraces
- 11:00 AM: Ubud Monkey Forest (Entry: ₹500)
- 01:00 PM: Traditional Balinese lunch
- 03:00 PM: Ubud Palace and Art Market
- 06:00 PM: Kecak Fire Dance show (₹800)
- Overnight at villa

Day 3: Temple Tour & Spa
- 08:00 AM: Tanah Lot Temple (Entry: ₹600)
- 11:00 AM: Uluwatu Temple cliff views
- 02:00 PM: Lunch with ocean view
- 04:00 PM: Couple spa session (2 hours)
- Evening: Jimbaran Beach seafood dinner
- Overnight at villa

Day 4: Water Sports & Beach
- 09:00 AM: Nusa Dua water sports
- Parasailing (₹1,500), Jet Ski (₹1,200)
- 12:00 PM: Beach club lunch
- 03:00 PM: Snorkeling at Blue Lagoon
- Evening: Sunset at Seminyak Beach
- Overnight at villa

Day 5: Island Hopping - Nusa Penida
- 07:00 AM: Speedboat to Nusa Penida (₹2,500)
- 09:00 AM: Kelingking Beach (T-Rex cliff)
- 11:00 AM: Angel's Billabong natural pool
- 01:00 PM: Lunch at local restaurant
- 03:00 PM: Crystal Bay snorkeling
- 05:00 PM: Return to Bali
- Overnight at villa

Day 6: Shopping & Relaxation
- 10:00 AM: Seminyak shopping streets
- 12:00 PM: Lunch at trendy cafe
- 02:00 PM: Pool relaxation at villa
- 06:00 PM: Romantic candlelight dinner
- Private photographer session (₹3,000)
- Overnight at villa

Day 7: Departure
- Leisure morning at villa
- 12:00 PM: Check-out
- Airport transfer
- Flight: SG 512 Bali to Delhi (02:00 PM - 07:00 PM) - ₹38,000"""
        },
        {
            "title": "Manali Adventure Trek", 
            "destination": destinations[2], 
            "category": "adventure", 
            "duration": "4-7", 
            "price": 15499,
            "price_per_person": 15499,
            "price_per_couple": 28999,
            "price_per_group": 54999,
            "emi_per_month": 2583,
            "description": "Thrilling 5-day adventure with trekking, rafting, paragliding in the Himalayas",
            "inclusions": "Hotel accommodation, Daily meals, Volvo bus from Delhi, All adventure activities, Professional guides, Safety equipment",
            "exclusions": "Personal expenses, Travel insurance, Additional activities, Monument fees",
            "itinerary": """Day 1: Delhi to Manali
- Volvo Bus: Delhi to Manali (06:00 PM - 08:00 AM+1) - ₹1,200
- Overnight journey in AC Volvo
- Distance: 540 km (14 hours)

Day 2: Arrival & Local Sightseeing
- 08:00 AM: Arrival and hotel check-in
- 10:00 AM: Breakfast and rest
- 12:00 PM: Hadimba Temple visit
- 02:00 PM: Lunch at local restaurant
- 03:00 PM: Vashisht hot springs
- 05:00 PM: Mall Road shopping
- 07:00 PM: Dinner at hotel
- Overnight at hotel

Day 3: Solang Valley Adventure
- 08:00 AM: Drive to Solang Valley (30 min)
- 09:00 AM: Paragliding (₹1,500)
- 10:30 AM: Zorbing (₹500)
- 12:00 PM: Lunch at valley cafe
- 02:00 PM: Cable car ride (₹800)
- 04:00 PM: ATV ride (₹700)
- 06:00 PM: Return to hotel
- Overnight at hotel

Day 4: River Rafting & Trekking
- 07:00 AM: Drive to Kullu (1 hour)
- 09:00 AM: River rafting on Beas (₹800)
- 12:00 PM: Lunch at riverside
- 02:00 PM: Trek to Bijli Mahadev (3 hours)
- 05:00 PM: Return to Manali
- Evening: Bonfire and BBQ dinner
- Overnight at hotel

Day 5: Rohtang Pass & Departure
- 05:00 AM: Early start to Rohtang Pass
- 08:00 AM: Reach Rohtang (13,050 ft)
- Snow activities: Skiing, snowboarding
- 12:00 PM: Lunch at dhaba
- 02:00 PM: Return to Manali
- 04:00 PM: Check-out
- 06:00 PM: Volvo to Delhi (₹1,200)
- Overnight journey"""
        },
    ]
    
    for pkg_data in packages_data:
        pkg_data['is_featured'] = True
        pkg_data['emi_available'] = True
        pkg_data['inclusions'] = "Hotel, Meals, Transport, Guide"
        pkg_data['exclusions'] = "Flights, Personal expenses"
        pkg_data['itinerary'] = "Day 1: Arrival\nDay 2: Sightseeing\nDay 3: Adventure activities\nDay 4: Departure"
        pkg_data['available_from'] = date.today()
        pkg_data['available_to'] = date.today() + timedelta(days=365)
        pkg_data['popularity_score'] = 100
        
        pkg, created = TourPackage.objects.get_or_create(
            title=pkg_data["title"],
            defaults=pkg_data
        )
        if created:
            print(f"✓ Created package: {pkg.title}")
        else:
            # Update existing package with new pricing
            for key, value in pkg_data.items():
                setattr(pkg, key, value)
            pkg.save()
            print(f"✓ Updated package: {pkg.title}")
    
    print("\nCreating sample banners...")
    
    banners_data = [
        {"title": "Summer Sale 2026", "subtitle": "Up to 50% off on selected packages", "order": 1},
        {"title": "Early Bird Offers", "subtitle": "Book 3 months in advance and save 30%", "order": 2},
        {"title": "Group Discounts", "subtitle": "Travel with friends and get special rates", "order": 3},
    ]
    
    for banner_data in banners_data:
        banner, created = Banner.objects.get_or_create(
            title=banner_data["title"],
            defaults=banner_data
        )
        if created:
            print(f"✓ Created banner: {banner.title}")
    
    print("\nCreating sample testimonials...")
    
    testimonials_data = [
        {"customer_name": "Sarah Johnson", "rating": 5, "review": "Amazing experience! The Bali tour was perfectly organized and exceeded all expectations.", "is_featured": True},
        {"customer_name": "Michael Chen", "rating": 5, "review": "TravelVibe made our honeymoon in Maldives unforgettable. Highly recommended!", "is_featured": True},
        {"customer_name": "Priya Sharma", "rating": 4, "review": "Great service and beautiful destinations. The Goa package was fantastic!", "is_featured": True},
        {"customer_name": "David Wilson", "rating": 5, "review": "Professional team, great prices, and wonderful memories. Will book again!", "is_featured": True},
        {"customer_name": "Emma Brown", "rating": 5, "review": "The Paris trip was magical. Everything was well-planned and executed perfectly.", "is_featured": True},
        {"customer_name": "Raj Patel", "rating": 4, "review": "Manali adventure was thrilling! Good value for money and excellent guides.", "is_featured": True},
    ]
    
    for test_data in testimonials_data:
        test, created = Testimonial.objects.get_or_create(
            customer_name=test_data["customer_name"],
            defaults=test_data
        )
        if created:
            print(f"✓ Created testimonial: {test.customer_name}")
    
    print("\n✅ Sample data population complete!")
    print("\nYou can now:")
    print("1. Run the server: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/")
    print("3. Login to admin: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    populate_data()
