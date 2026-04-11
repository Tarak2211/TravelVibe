import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from store.models import TourPackage

# Flight details for each package
flight_updates = {
    'Dubai Luxury Experience': {
        'itinerary': """Day 1: Arrival in Dubai
- Flight: Air India AI 995 (Delhi to Dubai)
- Departure: 02:00 AM from Indira Gandhi International Airport, Delhi
- Arrival: 04:30 AM at Dubai International Airport (Flight duration: 3 hours 30 minutes)
- Flight cost: ₹18,000 per person (included in package)
- Private transfer to 5-star hotel (Burj Al Arab or Atlantis The Palm)
- Check-in and freshen up
- Rest and relax after early morning flight
- Evening visit to Dubai Mall and Burj Khalifa
- Watch the spectacular Dubai Fountain show (7:00 PM & 8:00 PM shows)
- Dinner at a rooftop restaurant with Burj Khalifa views
- Overnight stay at hotel

Day 2: Modern Dubai Tour
- Breakfast at hotel (7:00 AM - 10:00 AM)
- Visit Burj Khalifa - At The Top (124th & 125th floor) - 10:00 AM slot
- Explore Dubai Mall - world's largest shopping mall
- Lunch at Dubai Mall (1:00 PM)
- Visit Dubai Marina and walk along the promenade (3:00 PM)
- Enjoy a Dhow Cruise dinner with live entertainment (8:00 PM - 10:00 PM)
- Return to hotel
- Overnight stay

Day 3: Desert Safari Adventure
- Breakfast at hotel
- Morning at leisure or optional activities
- Afternoon: Desert Safari pickup (3:00 PM)
- Dune bashing in 4x4 vehicles (3:30 PM - 4:30 PM)
- Camel riding experience
- Sandboarding
- Sunset photography in the desert (6:00 PM)
- BBQ dinner at Bedouin camp with belly dance show (7:30 PM - 9:00 PM)
- Return to hotel (9:30 PM)
- Overnight stay

Day 4: Departure
- Breakfast at hotel
- Check-out from hotel (11:00 AM)
- Last-minute shopping at Gold Souk or Spice Souk
- Transfer to Dubai International Airport (3:00 PM)
- Flight: Air India AI 996 (Dubai to Delhi)
- Departure: 08:45 PM from Dubai International Airport
- Arrival: 01:15 AM+1 at Delhi (Flight duration: 3 hours 30 minutes)
- Flight cost: ₹18,000 per person (included in package)
- Arrival in India with wonderful memories

Total Flight Cost: ₹36,000 per person (Round trip - INCLUDED in package price)
Airlines: Air India (Direct flights, no layovers)""",
    },
    
    'Manali Adventure Trek': {
        'itinerary': """Day 1: Arrival in Manali
- Flight: IndiGo 6E 2524 (Delhi to Bhuntar/Kullu)
- Departure: 06:30 AM from Indira Gandhi International Airport, Delhi
- Arrival: 07:45 AM at Bhuntar Airport (Flight duration: 1 hour 15 minutes)
- Flight cost: ₹4,500 per person (included in package)
- Transfer to Manali by taxi (50 km, 1.5 hours) - ₹1,500
- Arrive in Manali around 9:30 AM
- Check-in at hotel and rest
- Lunch at hotel (1:00 PM)
- Evening walk on Mall Road (5:00 PM)
- Visit Hadimba Devi Temple
- Explore local markets
- Dinner at hotel (8:00 PM)
- Overnight stay in Manali

Day 2: Manali Local Sightseeing
- Breakfast at hotel (8:00 AM)
- Visit Hadimba Temple and Manu Temple (9:00 AM)
- Explore Vashisht Village and hot water springs (11:00 AM)
- Visit Tibetan Monastery (12:30 PM)
- Lunch at local restaurant (1:30 PM)
- Visit Club House for adventure activities (3:00 PM)
- Evening at leisure on Mall Road (6:00 PM)
- Dinner at hotel (8:00 PM)
- Overnight stay

Day 3: Solang Valley Excursion
- Early breakfast (7:00 AM)
- Depart for Solang Valley (8:00 AM)
- Full day excursion to Solang Valley (14 km from Manali)
- Enjoy paragliding (₹2,500), zorbing (₹500), and horse riding (₹300)
- Cable car ride to snow point (₹700)
- Lunch at Solang Valley (1:00 PM)
- Photography and snow activities
- Return to Manali by evening (6:00 PM)
- Dinner at hotel (8:00 PM)
- Overnight stay

Day 4: Rohtang Pass Adventure
- Very early breakfast (5:00 AM)
- Depart for Rohtang Pass (5:30 AM)
- Full day trip to Rohtang Pass (51 km from Manali)
- Rohtang Pass permit: ₹500 per person (included)
- Enjoy snow activities - skiing (₹1,500), snowboarding (₹2,000)
- Visit Rahalla Falls en route
- Packed lunch
- Return to Manali by evening (7:00 PM)
- Farewell dinner (8:00 PM)
- Overnight stay

Day 5: Departure
- Breakfast at hotel (7:00 AM)
- Check-out (9:00 AM)
- Transfer to Bhuntar Airport (depart 9:30 AM, arrive 11:00 AM)
- Flight: IndiGo 6E 2525 (Bhuntar to Delhi)
- Departure: 01:00 PM from Bhuntar Airport
- Arrival: 02:15 PM at Delhi (Flight duration: 1 hour 15 minutes)
- Flight cost: ₹4,500 per person (included in package)
- Departure with beautiful memories

Total Flight Cost: ₹9,000 per person (Round trip - INCLUDED in package price)
Airlines: IndiGo (Direct flights)""",
    },
    
    'Goa Beach Paradise': {
        'itinerary': """Day 1: Arrival in Goa
- Flight: IndiGo 6E 6112 (Delhi to Goa)
- Departure: 09:15 AM from Indira Gandhi International Airport, Delhi
- Arrival: 11:45 AM at Goa International Airport (Flight duration: 2 hours 30 minutes)
- Flight cost: ₹5,500 per person (included in package)
- Transfer to beach resort in North Goa (45 minutes)
- Check-in and freshen up (1:00 PM)
- Lunch at resort (2:00 PM)
- Relax at the beach (3:00 PM)
- Evening visit to Calangute Beach (5:00 PM)
- Sunset at Baga Beach (6:30 PM)
- Dinner at beach shack (8:00 PM)
- Overnight stay at resort

Day 2: North Goa Beaches Tour
- Breakfast at resort (8:00 AM)
- Visit Fort Aguada - historic Portuguese fort (9:30 AM)
- Explore Candolim Beach (11:00 AM)
- Lunch at beach restaurant (1:00 PM)
- Visit Anjuna Beach and Anjuna Flea Market (3:00 PM)
- Evening at Vagator Beach (5:30 PM)
- Watch sunset at Chapora Fort (6:30 PM)
- Dinner at Tito's Lane, Baga (8:00 PM)
- Overnight stay

Day 3: South Goa Exploration
- Breakfast at resort (8:00 AM)
- Check-out and transfer to South Goa resort (9:00 AM)
- Visit Basilica of Bom Jesus - UNESCO World Heritage Site (10:30 AM)
- Explore Se Cathedral (11:30 AM)
- Lunch at Panjim (1:00 PM)
- Visit Miramar Beach (2:30 PM)
- Check-in at South Goa resort (4:00 PM)
- Evening at Colva Beach (5:30 PM)
- Dinner at resort (8:00 PM)
- Overnight stay

Day 4: Water Sports & Beach Activities
- Breakfast at resort (8:00 AM)
- Full day at Palolem Beach (9:00 AM)
- Water sports: Jet skiing (₹1,500), parasailing (₹2,500), banana boat ride (₹500)
- Lunch at beach shack (1:00 PM)
- Dolphin watching boat trip (3:00 PM) - ₹1,000
- Relax on the beach (4:30 PM)
- Sunset photography (6:30 PM)
- Farewell dinner at beach restaurant (8:00 PM)
- Overnight stay

Day 5: Departure
- Breakfast at resort (8:00 AM)
- Check-out (10:00 AM)
- Last-minute beach visit or shopping
- Transfer to Goa Airport (12:00 PM)
- Flight: IndiGo 6E 6113 (Goa to Delhi)
- Departure: 03:30 PM from Goa International Airport
- Arrival: 06:00 PM at Delhi (Flight duration: 2 hours 30 minutes)
- Flight cost: ₹5,500 per person (included in package)
- Arrival in Delhi

Total Flight Cost: ₹11,000 per person (Round trip - INCLUDED in package price)
Airlines: IndiGo (Direct flights)""",
    },
    
    'Kerala Backwaters Cruise': {
        'itinerary': """Day 1: Arrival in Cochin
- Flight: Air India AI 440 (Delhi to Cochin)
- Departure: 06:00 AM from Indira Gandhi International Airport, Delhi
- Arrival: 09:15 AM at Cochin International Airport (Flight duration: 3 hours 15 minutes)
- Flight cost: ₹6,500 per person (included in package)
- Transfer to hotel in Fort Kochi (1 hour)
- Check-in and freshen up (11:00 AM)
- Lunch at hotel (1:00 PM)
- Rest and relax
- Evening visit to Fort Kochi (4:00 PM)
- Watch Chinese Fishing Nets (5:00 PM)
- Explore Jew Town and Synagogue (5:30 PM)
- Kathakali dance show (6:30 PM - 8:00 PM) - ₹500
- Dinner at local restaurant (8:30 PM)
- Overnight stay in Cochin

Day 2: Cochin to Munnar
- Breakfast at hotel (7:00 AM)
- Check-out and drive to Munnar (8:00 AM) - 130 km, 4 hours
- En route visit Cheeyappara Waterfalls (10:00 AM)
- Visit Valara Waterfalls (10:30 AM)
- Arrive in Munnar (12:00 PM)
- Check-in at Munnar resort
- Lunch at resort (1:00 PM)
- Rest and relax
- Evening visit to Tea Gardens (4:00 PM)
- Tea tasting session (5:00 PM)
- Dinner at resort (8:00 PM)
- Overnight stay in Munnar

Day 3: Munnar Sightseeing
- Early breakfast (7:00 AM)
- Visit Eravikulam National Park (8:00 AM) - Entry ₹600
- See Nilgiri Tahr (mountain goats)
- Visit Mattupetty Dam (10:30 AM)
- Visit Echo Point (11:30 AM)
- Lunch at local restaurant (1:00 PM)
- Visit Tea Museum (2:30 PM) - Entry ₹125
- Explore Kundala Lake (4:00 PM)
- Return to resort (6:00 PM)
- Dinner and overnight stay (8:00 PM)

Day 4: Munnar to Alleppey - Houseboat Experience
- Breakfast at resort (7:00 AM)
- Check-out and drive to Alleppey (8:00 AM) - 170 km, 5 hours
- Arrive at Alleppey (1:00 PM)
- Check-in to traditional Kerala houseboat (1:30 PM)
- Welcome drink and lunch on houseboat (2:00 PM)
- Cruise through backwaters
- Watch village life along the canals
- Sunset on the backwaters (6:00 PM)
- Dinner on houseboat (8:00 PM)
- Overnight stay on houseboat

Day 5: Alleppey to Cochin - Departure
- Breakfast on houseboat (8:00 AM)
- Check-out from houseboat (9:00 AM)
- Drive to Cochin (55 km, 1.5 hours)
- Arrive in Cochin (10:30 AM)
- Visit Marine Drive and Lulu Mall for shopping (11:00 AM)
- Lunch at Cochin (1:00 PM)
- Transfer to Cochin Airport (2:30 PM)
- Flight: Air India AI 441 (Cochin to Delhi)
- Departure: 05:00 PM from Cochin International Airport
- Arrival: 08:15 PM at Delhi (Flight duration: 3 hours 15 minutes)
- Flight cost: ₹6,500 per person (included in package)
- Arrival in Delhi with wonderful memories

Total Flight Cost: ₹13,000 per person (Round trip - INCLUDED in package price)
Airlines: Air India (Direct flights)""",
    },
}

# Update packages
print("Adding flight details to packages...")
for title, data in flight_updates.items():
    try:
        package = TourPackage.objects.get(title=title)
        package.itinerary = data['itinerary']
        package.save()
        print(f"✓ Updated: {title}")
    except TourPackage.DoesNotExist:
        print(f"✗ Package not found: {title}")

print("\nDone! All packages now have complete flight details.")
