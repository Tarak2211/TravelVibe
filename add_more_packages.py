"""
Add more detailed packages
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from store.models import Destination, TourPackage
from datetime import date, timedelta

def add_packages():
    print("Adding more packages...")
    
    # Get destinations
    kerala = Destination.objects.get(name="Kerala")
    jaipur = Destination.objects.get(name="Jaipur")
    thailand = Destination.objects.get(name="Thailand")
    switzerland = Destination.objects.get(name="Switzerland")
    singapore = Destination.objects.get(name="Singapore")
    shimla = Destination.objects.get(name="Shimla")
    dubai = Destination.objects.get(name="Dubai")
    paris = Destination.objects.get(name="Paris")
    maldives = Destination.objects.get(name="Maldives")
    
    more_packages = [
        {
            "title": "Kerala Backwaters Cruise",
            "destination": kerala,
            "category": "family",
            "duration": "4-7",
            "price": 22999,
            "price_per_person": 22999,
            "price_per_couple": 42999,
            "price_per_group": 79999,
            "emi_per_month": 3833,
            "description": "Experience God's own country with houseboat stay and Ayurvedic spa",
            "inclusions": "Houseboat accommodation, All meals, Airport transfers, Ayurvedic massage, Kathakali dance show",
            "exclusions": "Airfare, Personal expenses, Additional activities",
            "itinerary": """Day 1: Arrival Cochin
- Flight: 6E 345 Delhi to Cochin (07:00 AM - 10:30 AM) - ₹5,500
- Fort Kochi sightseeing
- Chinese fishing nets, St. Francis Church
- Kathakali dance show (₹500)

Day 2: Munnar Hill Station
- Drive to Munnar (4 hours)
- Tea plantation visit
- Mattupetty Dam, Echo Point
- Overnight at resort

Day 3: Thekkady Wildlife
- Periyar Wildlife Sanctuary
- Boat safari (₹300)
- Spice plantation tour
- Elephant ride (₹800)

Day 4: Alleppey Houseboat
- Check-in to houseboat at 12:00 PM
- Cruise through backwaters
- Traditional Kerala meals
- Overnight on houseboat

Day 5: Departure
- Check-out at 09:00 AM
- Cochin airport transfer
- Flight: 6E 346 Cochin to Delhi (02:00 PM - 05:30 PM) - ₹6,000""",
            "is_featured": True,
            "emi_available": True,
            "available_from": date.today(),
            "available_to": date.today() + timedelta(days=365),
            "popularity_score": 95
        },
        {
            "title": "Jaipur Royal Heritage Tour",
            "destination": jaipur,
            "category": "family",
            "duration": "1-3",
            "price": 8999,
            "price_per_person": 8999,
            "price_per_couple": 16999,
            "price_per_group": 31999,
            "emi_per_month": 1500,
            "description": "Explore the Pink City's majestic forts and palaces",
            "inclusions": "3-star hotel, Daily breakfast, All monument entries, City tour guide",
            "exclusions": "Train fare, Lunch and dinner, Personal expenses",
            "itinerary": """Day 1: Delhi to Jaipur
- Train: Shatabdi Express (06:00 AM - 10:30 AM) - ₹800
- Check-in at hotel
- City Palace visit (Entry: ₹700)
- Jantar Mantar observatory (₹200)
- Hawa Mahal photo stop
- Evening: Chokhi Dhani village (₹900)

Day 2: Amber Fort & Shopping
- 09:00 AM: Amber Fort (Entry: ₹500)
- Elephant ride to fort (₹1,200)
- Jaigarh Fort cannon view
- Lunch at traditional restaurant
- Johari Bazaar shopping
- Bapu Bazaar textiles

Day 3: Departure
- Morning: Jal Mahal lake palace
- Birla Temple visit
- Train: Shatabdi (04:00 PM - 08:30 PM) - ₹800""",
            "is_featured": True,
            "emi_available": True,
            "available_from": date.today(),
            "available_to": date.today() + timedelta(days=365),
            "popularity_score": 90
        },
        {
            "title": "Thailand Beach Paradise",
            "destination": thailand,
            "category": "honeymoon",
            "duration": "4-7",
            "price": 65999,
            "price_per_person": 65999,
            "price_per_couple": 125999,
            "price_per_group": 245999,
            "emi_per_month": 10999,
            "description": "Bangkok and Pattaya with beaches, temples, and nightlife",
            "inclusions": "4-star hotels, Daily breakfast, Airport transfers, City tours, Coral Island trip",
            "exclusions": "International flights, Visa (₹2,500), Lunch/dinner, Personal expenses",
            "itinerary": """Day 1: Arrival Bangkok
- Flight: TG 331 Delhi to Bangkok (02:00 AM - 07:30 AM) - ₹18,000
- Hotel check-in
- Grand Palace visit (₹500)
- Wat Pho reclining Buddha
- Evening: Chao Phraya river cruise (₹800)

Day 2: Bangkok City Tour
- Safari World & Marine Park (₹1,500)
- Lunch at park
- Shopping at MBK Center
- Evening: Asiatique night market

Day 3: Pattaya Transfer
- Drive to Pattaya (2 hours)
- Check-in at beach resort
- Pattaya Beach relaxation
- Evening: Alcazar Cabaret show (₹1,200)

Day 4: Coral Island
- Speedboat to Coral Island (₹1,800)
- Parasailing (₹800), Jet Ski (₹600)
- Underwater sea walk (₹2,500)
- Beach lunch
- Return to hotel

Day 5: Bangkok & Departure
- Return to Bangkok
- Last minute shopping
- Flight: TG 332 Bangkok to Delhi (09:00 PM - 01:00 AM+1) - ₹20,000""",
            "is_featured": True,
            "emi_available": True,
            "available_from": date.today(),
            "available_to": date.today() + timedelta(days=365),
            "popularity_score": 92
        },
    ]
    
    for pkg_data in more_packages:
        pkg, created = TourPackage.objects.update_or_create(
            title=pkg_data["title"],
            defaults=pkg_data
        )
        if created:
            print(f"✓ Created: {pkg.title}")
        else:
            print(f"✓ Updated: {pkg.title}")
    
    print("\n✅ Additional packages added!")

if __name__ == "__main__":
    add_packages()
