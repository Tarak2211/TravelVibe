"""
Add comprehensive destinations and packages
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from store.models import Destination, TourPackage
from datetime import date, timedelta

def add_all_destinations():
    print("Adding comprehensive destinations and packages...")
    
    # Indian Destinations
    indian_destinations = [
        {"name": "Udaipur", "country": "India", "description": "City of Lakes with royal palaces", "is_trending": True},
        {"name": "Rishikesh", "country": "India", "description": "Yoga capital and adventure sports hub", "is_trending": True},
        {"name": "Andaman", "country": "India", "description": "Pristine beaches and coral reefs", "is_trending": True},
        {"name": "Leh Ladakh", "country": "India", "description": "High altitude desert with monasteries", "is_trending": True},
        {"name": "Ooty", "country": "India", "description": "Queen of hill stations", "is_trending": True},
        {"name": "Darjeeling", "country": "India", "description": "Tea gardens and Himalayan views", "is_trending": True},
        {"name": "Varanasi", "country": "India", "description": "Spiritual capital on Ganges", "is_trending": True},
        {"name": "Agra", "country": "India", "description": "Home of Taj Mahal", "is_trending": True},
        {"name": "Coorg", "country": "India", "description": "Scotland of India with coffee estates", "is_trending": True},
        {"name": "Mysore", "country": "India", "description": "Palace city with rich heritage", "is_trending": True},
    ]
    
    # International Destinations
    international_destinations = [
        {"name": "Malaysia", "country": "Malaysia", "description": "Petronas Towers and tropical islands", "is_trending": True},
        {"name": "Vietnam", "country": "Vietnam", "description": "Ha Long Bay and ancient temples", "is_trending": True},
        {"name": "Turkey", "country": "Turkey", "description": "Istanbul and Cappadocia hot air balloons", "is_trending": True},
        {"name": "Greece", "country": "Greece", "description": "Santorini sunsets and ancient ruins", "is_trending": True},
        {"name": "Italy", "country": "Italy", "description": "Rome, Venice and Tuscany", "is_trending": True},
        {"name": "Spain", "country": "Spain", "description": "Barcelona and Madrid culture", "is_trending": True},
        {"name": "Australia", "country": "Australia", "description": "Sydney Opera House and Great Barrier Reef", "is_trending": True},
        {"name": "New Zealand", "country": "New Zealand", "description": "Lord of the Rings landscapes", "is_trending": True},
        {"name": "Japan", "country": "Japan", "description": "Tokyo and Mount Fuji", "is_trending": True},
        {"name": "South Korea", "country": "South Korea", "description": "Seoul and K-pop culture", "is_trending": True},
        {"name": "Mauritius", "country": "Mauritius", "description": "Beach paradise in Indian Ocean", "is_trending": True},
    ]
    
    all_destinations = indian_destinations + international_destinations
    
    created_destinations = {}
    for dest_data in all_destinations:
        dest, created = Destination.objects.get_or_create(
            name=dest_data["name"],
            defaults=dest_data
        )
        created_destinations[dest.name] = dest
        if created:
            print(f"✓ Created destination: {dest.name}")
        else:
            print(f"  Already exists: {dest.name}")
    
    # Add detailed packages
    packages_data = [
        # Indian Packages
        {
            "title": "Udaipur Royal Heritage",
            "destination": created_destinations["Udaipur"],
            "category": "honeymoon",
            "duration": "1-3",
            "price": 12999,
            "price_per_person": 12999,
            "price_per_couple": 24999,
            "price_per_group": 47999,
            "emi_per_month": 2167,
            "description": "Explore the City of Lakes with palace stays and boat rides",
            "inclusions": "Heritage hotel stay, Lake Pichola boat ride, City Palace entry, All meals, Airport transfers",
            "exclusions": "Airfare, Personal expenses, Additional activities",
            "itinerary": """Day 1: Arrival Udaipur
- Flight: 6E 234 Delhi to Udaipur (08:00 AM - 09:30 AM) - ₹3,500
- Check-in at heritage hotel
- City Palace visit (Entry: ₹300)
- Jagdish Temple
- Evening: Lake Pichola boat ride (₹500)
- Sunset at Ambrai Ghat

Day 2: Lake Tour & Shopping
- Fateh Sagar Lake
- Saheliyon ki Bari garden (Entry: ₹50)
- Monsoon Palace sunset (Entry: ₹80)
- Shopping at Hathi Pol Bazaar
- Cultural show at Bagore ki Haveli (₹150)

Day 3: Departure
- Morning: Jag Mandir island palace
- Lunch at lakeside restaurant
- Flight: 6E 235 Udaipur to Delhi (03:00 PM - 04:30 PM) - ₹3,800"""
        },
        {
            "title": "Rishikesh Adventure Camp",
            "destination": created_destinations["Rishikesh"],
            "category": "adventure",
            "duration": "1-3",
            "price": 9999,
            "price_per_person": 9999,
            "price_per_couple": 18999,
            "price_per_group": 35999,
            "emi_per_month": 1667,
            "description": "Yoga, rafting, and camping by the Ganges",
            "inclusions": "Riverside camping, All meals, River rafting, Bungee jumping, Yoga sessions",
            "exclusions": "Transport from Delhi, Personal expenses, Additional activities",
            "itinerary": """Day 1: Delhi to Rishikesh
- Volvo Bus: Delhi to Rishikesh (06:00 AM - 12:00 PM) - ₹800
- Check-in at riverside camp
- Evening: Ganga Aarti at Triveni Ghat
- Bonfire and dinner

Day 2: Adventure Activities
- 06:00 AM: Sunrise yoga session
- 09:00 AM: White water rafting (16 km) - ₹800
- 12:00 PM: Lunch at camp
- 02:00 PM: Bungee jumping (₹3,500)
- 04:00 PM: Flying fox (₹1,500)
- Evening: Cliff jumping at Shivpuri

Day 3: Spiritual & Departure
- Morning: Beatles Ashram visit (₹150)
- Lakshman Jhula and Ram Jhula
- Lunch at German Bakery
- Volvo: Rishikesh to Delhi (03:00 PM - 09:00 PM) - ₹800"""
        },
        {
            "title": "Andaman Beach Paradise",
            "destination": created_destinations["Andaman"],
            "category": "honeymoon",
            "duration": "4-7",
            "price": 45999,
            "price_per_person": 45999,
            "price_per_couple": 89999,
            "price_per_group": 175999,
            "emi_per_month": 7667,
            "description": "Pristine beaches, scuba diving, and island hopping",
            "inclusions": "Beach resort stay, All meals, Island tours, Scuba diving, Airport transfers",
            "exclusions": "Flights, Personal expenses, Water sports",
            "itinerary": """Day 1: Port Blair Arrival
- Flight: 6E 789 Delhi to Port Blair (05:00 AM - 10:30 AM) - ₹12,000
- Cellular Jail visit (Entry: ₹30)
- Light & Sound show (₹250)
- Corbyn's Cove Beach

Day 2: Havelock Island
- Ferry to Havelock (₹1,500)
- Radhanagar Beach (Asia's best beach)
- Beach resort check-in
- Sunset photography

Day 3: Water Activities
- Scuba diving at Elephant Beach (₹4,500)
- Snorkeling (₹1,500)
- Kayaking through mangroves (₹1,000)
- Beach relaxation

Day 4: Neil Island
- Ferry to Neil Island (₹800)
- Natural Bridge
- Bharatpur Beach
- Laxmanpur Beach sunset
- Return to Havelock

Day 5: Return to Port Blair
- Ferry back to Port Blair
- Shopping at Aberdeen Bazaar
- Seafood dinner
- Flight: 6E 790 Port Blair to Delhi (08:00 PM - 01:30 AM+1) - ₹13,500"""
        },
        {
            "title": "Leh Ladakh Bike Expedition",
            "destination": created_destinations["Leh Ladakh"],
            "category": "adventure",
            "duration": "8-14",
            "price": 35999,
            "price_per_person": 35999,
            "price_per_couple": 69999,
            "price_per_group": 135999,
            "emi_per_month": 6000,
            "description": "Epic bike journey through world's highest motorable roads",
            "inclusions": "Royal Enfield bike rental, Accommodation, Permits, Fuel, Mechanic support",
            "exclusions": "Flights, Meals, Personal expenses, Bike damage",
            "itinerary": """Day 1: Leh Arrival & Acclimatization
- Flight: 6E 456 Delhi to Leh (06:00 AM - 07:30 AM) - ₹8,000
- Rest day for altitude adjustment
- Leh Palace and Shanti Stupa
- Local market exploration

Day 2: Leh to Nubra Valley
- Khardung La Pass (18,380 ft) - World's highest motorable road
- Distance: 120 km (6 hours)
- Diskit Monastery
- Hunder sand dunes
- Double hump camel ride (₹500)

Day 3: Nubra to Pangong Lake
- Via Shyok route
- Distance: 160 km (7 hours)
- Pangong Tso (14,270 ft)
- 3 Idiots movie location
- Lakeside camping

Day 4: Pangong to Leh
- Sunrise at Pangong
- Return via Chang La Pass (17,590 ft)
- Distance: 140 km (6 hours)
- Thiksey Monastery
- Shey Palace

Day 5: Leh to Lamayuru
- Magnetic Hill
- Gurudwara Pathar Sahib
- Lamayuru Monastery (Moonland)
- Distance: 125 km

Day 6: Lamayuru to Leh
- Return journey
- Alchi Monastery
- Confluence of Indus and Zanskar
- Rafting option (₹1,500)

Day 7: Departure
- Flight: 6E 457 Leh to Delhi (08:00 AM - 09:30 AM) - ₹9,000"""
        },
        # International Packages
        {
            "title": "Malaysia Twin Cities",
            "destination": created_destinations["Malaysia"],
            "category": "family",
            "duration": "4-7",
            "price": 55999,
            "price_per_person": 55999,
            "price_per_couple": 109999,
            "price_per_group": 215999,
            "emi_per_month": 9333,
            "description": "Kuala Lumpur and Penang with theme parks and beaches",
            "inclusions": "4-star hotels, Daily breakfast, City tours, Theme park tickets, Airport transfers",
            "exclusions": "International flights, Visa (₹3,000), Lunch/dinner, Personal expenses",
            "itinerary": """Day 1: Kuala Lumpur Arrival
- Flight: AI 316 Delhi to KL (11:00 PM - 07:00 AM+1) - ₹22,000
- Petronas Twin Towers visit (₹800)
- KLCC Park and Aquarium
- Batu Caves (Free entry)
- Evening: Bukit Bintang shopping

Day 2: Genting Highlands
- Cable car to Genting (₹1,200)
- Theme park and casino
- Chin Swee Temple
- Strawberry farm
- Return to KL

Day 3: Penang Transfer
- Flight: KL to Penang (1 hour) - ₹3,500
- Georgetown heritage walk
- Street art photography
- Penang Hill funicular (₹400)
- Kek Lok Si Temple

Day 4: Penang Beaches
- Batu Ferringhi Beach
- Water sports (₹2,000)
- Tropical Spice Garden (₹300)
- Night market shopping

Day 5: Return to KL & Departure
- Flight: Penang to KL (1 hour) - ₹3,500
- Last minute shopping
- Flight: AI 317 KL to Delhi (09:00 PM - 01:00 AM+1) - ₹24,000"""
        },
        {
            "title": "Vietnam Heritage Trail",
            "destination": created_destinations["Vietnam"],
            "category": "family",
            "duration": "4-7",
            "price": 48999,
            "price_per_person": 48999,
            "price_per_couple": 95999,
            "price_per_group": 189999,
            "emi_per_month": 8167,
            "description": "Hanoi, Ha Long Bay cruise, and Ho Chi Minh City",
            "inclusions": "Hotels, Daily breakfast, Ha Long Bay cruise, City tours, Transfers",
            "exclusions": "International flights, Visa (₹2,500), Lunch/dinner, Personal expenses",
            "itinerary": """Day 1: Hanoi Arrival
- Flight: VN 612 Delhi to Hanoi (10:00 AM - 04:00 PM) - ₹18,000
- Old Quarter walking tour
- Hoan Kiem Lake
- Water puppet show (₹500)
- Street food tour

Day 2: Ha Long Bay Cruise
- Drive to Ha Long Bay (3.5 hours)
- Luxury cruise check-in
- Kayaking and swimming
- Cave exploration
- Overnight on cruise

Day 3: Ha Long to Hanoi
- Tai Chi on deck
- Return to Hanoi
- Temple of Literature
- Ho Chi Minh Mausoleum
- Train Street photography

Day 4: Fly to Ho Chi Minh City
- Flight: Hanoi to HCMC (2 hours) - ₹5,000
- Cu Chi Tunnels tour (₹800)
- War Remnants Museum
- Ben Thanh Market
- Saigon River cruise

Day 5: Mekong Delta & Departure
- Mekong Delta day trip (₹1,500)
- Floating markets
- Coconut candy workshop
- Flight: VN 613 HCMC to Delhi (11:00 PM - 04:00 AM+1) - ₹20,000"""
        },
        {
            "title": "Turkey Grand Tour",
            "destination": created_destinations["Turkey"],
            "category": "honeymoon",
            "duration": "8-14",
            "price": 125999,
            "price_per_person": 125999,
            "price_per_couple": 249999,
            "price_per_group": 495999,
            "emi_per_month": 21000,
            "description": "Istanbul, Cappadocia hot air balloons, and Pamukkale",
            "inclusions": "4-star hotels, Daily breakfast, Hot air balloon ride, All tours, Transfers",
            "exclusions": "International flights, Visa (₹5,000), Lunch/dinner, Personal expenses",
            "itinerary": """Day 1: Istanbul Arrival
- Flight: TK 716 Delhi to Istanbul (02:00 AM - 06:30 AM) - ₹35,000
- Hagia Sophia (Entry: ₹1,000)
- Blue Mosque
- Topkapi Palace (₹800)
- Grand Bazaar shopping

Day 2: Istanbul Bosphorus
- Bosphorus cruise (₹1,500)
- Dolmabahce Palace (₹600)
- Taksim Square
- Galata Tower (₹400)
- Turkish dinner show (₹2,500)

Day 3: Fly to Cappadocia
- Flight: Istanbul to Kayseri (1.5 hours) - ₹6,000
- Goreme Open Air Museum (₹800)
- Fairy chimneys
- Underground city
- Cave hotel check-in

Day 4: Hot Air Balloon & Tour
- 05:00 AM: Hot air balloon ride (₹12,000)
- Breakfast at hotel
- Pigeon Valley
- Pottery workshop
- ATV sunset tour (₹2,000)

Day 5: Pamukkale
- Drive to Pamukkale (6 hours)
- Cotton Castle travertines
- Hierapolis ancient city
- Thermal pools (₹500)

Day 6: Return to Istanbul
- Flight: Denizli to Istanbul (1.5 hours) - ₹6,000
- Free time for shopping
- Spice Bazaar
- Turkish bath (₹3,000)

Day 7: Departure
- Flight: TK 717 Istanbul to Delhi (01:00 PM - 10:00 PM) - ₹38,000"""
        },
        {
            "title": "Greece Island Hopping",
            "destination": created_destinations["Greece"],
            "category": "honeymoon",
            "duration": "8-14",
            "price": 155999,
            "price_per_person": 155999,
            "price_per_couple": 309999,
            "price_per_group": 615999,
            "emi_per_month": 26000,
            "description": "Athens, Santorini sunsets, and Mykonos beaches",
            "inclusions": "Hotels, Daily breakfast, Ferry tickets, Island tours, Transfers",
            "exclusions": "International flights, Visa (₹6,000), Lunch/dinner, Personal expenses",
            "itinerary": """Day 1: Athens Arrival
- Flight: EK 512 Delhi to Athens (via Dubai) - ₹45,000
- Acropolis and Parthenon (₹1,500)
- Plaka neighborhood
- Syntagma Square
- Greek dinner at taverna

Day 2: Athens Sightseeing
- Ancient Agora (₹600)
- Temple of Zeus
- Panathenaic Stadium
- National Archaeological Museum (₹800)
- Monastiraki flea market

Day 3: Ferry to Santorini
- Ferry: Athens to Santorini (8 hours) - ₹5,000
- Fira town exploration
- Caldera views
- Sunset at Oia village

Day 4: Santorini Tour
- Red Beach
- Akrotiri archaeological site (₹1,000)
- Wine tasting tour (₹3,000)
- Catamaran cruise (₹5,000)
- Sunset dinner

Day 5: Ferry to Mykonos
- Ferry: Santorini to Mykonos (3 hours) - ₹4,000
- Little Venice
- Windmills photography
- Paradise Beach
- Beach club party

Day 6: Mykonos Beaches
- Super Paradise Beach
- Water sports (₹3,000)
- Delos island day trip (₹2,500)
- Shopping in Mykonos town

Day 7: Return to Athens & Departure
- Ferry: Mykonos to Athens (5 hours) - ₹4,500
- Flight: EK 513 Athens to Delhi (via Dubai) - ₹48,000"""
        },
        {
            "title": "Japan Cherry Blossom Tour",
            "destination": created_destinations["Japan"],
            "category": "family",
            "duration": "8-14",
            "price": 185999,
            "price_per_person": 185999,
            "price_per_couple": 369999,
            "price_per_group": 735999,
            "emi_per_month": 31000,
            "description": "Tokyo, Mount Fuji, Kyoto temples, and Osaka",
            "inclusions": "Hotels, Daily breakfast, JR Pass, All tours, Transfers",
            "exclusions": "International flights, Visa (₹4,000), Lunch/dinner, Personal expenses",
            "itinerary": """Day 1: Tokyo Arrival
- Flight: NH 837 Delhi to Tokyo (11:00 PM - 10:00 AM+1) - ₹55,000
- Shibuya Crossing
- Harajuku fashion street
- Meiji Shrine
- Tokyo Tower (₹1,200)

Day 2: Tokyo Disney
- Tokyo Disneyland (₹6,500)
- Full day at theme park
- Parade and fireworks

Day 3: Mount Fuji Day Trip
- Bullet train to Fuji (₹8,000 - covered in JR Pass)
- 5th Station visit
- Lake Kawaguchi
- Hakone hot springs
- Return to Tokyo

Day 4: Tokyo to Kyoto
- Bullet train (2.5 hours)
- Fushimi Inari Shrine
- Thousand torii gates
- Gion geisha district
- Traditional tea ceremony (₹2,000)

Day 5: Kyoto Temples
- Kinkaku-ji Golden Pavilion (₹500)
- Arashiyama Bamboo Grove
- Monkey Park (₹600)
- Nishiki Market

Day 6: Osaka
- Train to Osaka (1 hour)
- Osaka Castle (₹800)
- Dotonbori food street
- Umeda Sky Building (₹1,500)
- Street food tour

Day 7: Departure
- Last minute shopping
- Flight: NH 838 Osaka to Delhi (10:00 AM - 04:00 PM) - ₹58,000"""
        },
    ]
    
    for pkg_data in packages_data:
        pkg_data['is_featured'] = True
        pkg_data['emi_available'] = True
        pkg_data['available_from'] = date.today()
        pkg_data['available_to'] = date.today() + timedelta(days=365)
        pkg_data['popularity_score'] = 90
        
        pkg, created = TourPackage.objects.update_or_create(
            title=pkg_data["title"],
            defaults=pkg_data
        )
        if created:
            print(f"✓ Created package: {pkg.title}")
        else:
            print(f"✓ Updated package: {pkg.title}")
    
    print("\n✅ All destinations and packages added successfully!")
    print(f"\nTotal Destinations: {Destination.objects.count()}")
    print(f"Total Packages: {TourPackage.objects.count()}")

if __name__ == "__main__":
    add_all_destinations()
