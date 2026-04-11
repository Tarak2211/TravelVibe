import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelvibe.settings')
django.setup()

from store.models import TourPackage

# Detailed itineraries for each package
itineraries = {
    'Dubai Luxury Experience': """Day 1: Arrival in Dubai
- Arrive at Dubai International Airport
- Private transfer to 5-star hotel (Burj Al Arab or Atlantis The Palm)
- Check-in and freshen up
- Evening visit to Dubai Mall and Burj Khalifa
- Watch the spectacular Dubai Fountain show
- Dinner at a rooftop restaurant with Burj Khalifa views
- Overnight stay at hotel

Day 2: Modern Dubai Tour
- Breakfast at hotel
- Visit Burj Khalifa - At The Top (124th & 125th floor)
- Explore Dubai Mall - world's largest shopping mall
- Lunch at Dubai Mall
- Visit Dubai Marina and walk along the promenade
- Enjoy a Dhow Cruise dinner with live entertainment
- Return to hotel
- Overnight stay

Day 3: Desert Safari Adventure
- Breakfast at hotel
- Morning at leisure or optional activities
- Afternoon: Desert Safari pickup (3:00 PM)
- Dune bashing in 4x4 vehicles
- Camel riding experience
- Sandboarding
- Sunset photography in the desert
- BBQ dinner at Bedouin camp with belly dance show
- Return to hotel (9:00 PM)
- Overnight stay

Day 4: Departure
- Breakfast at hotel
- Check-out from hotel
- Last-minute shopping at Gold Souk or Spice Souk (if time permits)
- Transfer to Dubai International Airport
- Departure with wonderful memories""",

    'Manali Adventure Trek': """Day 1: Arrival in Manali
- Arrive at Manali bus stand or Bhuntar Airport
- Transfer to hotel in Manali
- Check-in and rest
- Evening walk on Mall Road
- Visit Hadimba Devi Temple
- Explore local markets
- Dinner at hotel
- Overnight stay in Manali

Day 2: Manali Local Sightseeing
- Breakfast at hotel
- Visit Hadimba Temple and Manu Temple
- Explore Vashisht Village and hot water springs
- Visit Tibetan Monastery
- Lunch at local restaurant
- Visit Club House for adventure activities
- Evening at leisure on Mall Road
- Dinner at hotel
- Overnight stay

Day 3: Solang Valley Excursion
- Early breakfast
- Full day excursion to Solang Valley (14 km from Manali)
- Enjoy paragliding, zorbing, and horse riding
- Cable car ride to snow point
- Lunch at Solang Valley
- Photography and snow activities
- Return to Manali by evening
- Dinner at hotel
- Overnight stay

Day 4: Rohtang Pass Adventure
- Very early breakfast (5:00 AM)
- Full day trip to Rohtang Pass (51 km from Manali)
- Enjoy snow activities - skiing, snowboarding
- Visit Rahalla Falls en route
- Packed lunch
- Return to Manali by evening
- Farewell dinner
- Overnight stay

Day 5: Departure
- Breakfast at hotel
- Check-out
- Transfer to Bhuntar Airport or Manali bus stand
- Departure with beautiful memories""",

    'Goa Beach Paradise': """Day 1: Arrival in Goa
- Arrive at Goa International Airport
- Transfer to beach resort in North Goa
- Check-in and freshen up
- Relax at the beach
- Evening visit to Calangute Beach
- Sunset at Baga Beach
- Dinner at beach shack
- Overnight stay at resort

Day 2: North Goa Beaches Tour
- Breakfast at resort
- Visit Fort Aguada - historic Portuguese fort
- Explore Candolim Beach
- Lunch at beach restaurant
- Visit Anjuna Beach and Anjuna Flea Market
- Evening at Vagator Beach
- Watch sunset at Chapora Fort
- Dinner at Tito's Lane, Baga
- Overnight stay

Day 3: South Goa Exploration
- Breakfast at resort
- Check-out and transfer to South Goa resort
- Visit Basilica of Bom Jesus - UNESCO World Heritage Site
- Explore Se Cathedral
- Lunch at Panjim
- Visit Miramar Beach
- Check-in at South Goa resort
- Evening at Colva Beach
- Dinner at resort
- Overnight stay

Day 4: Water Sports & Beach Activities
- Breakfast at resort
- Full day at Palolem Beach
- Water sports: Jet skiing, parasailing, banana boat ride
- Lunch at beach shack
- Dolphin watching boat trip
- Relax on the beach
- Sunset photography
- Farewell dinner at beach restaurant
- Overnight stay

Day 5: Departure
- Breakfast at resort
- Check-out
- Last-minute beach visit or shopping
- Transfer to Goa Airport
- Departure""",

    'Kerala Backwaters Cruise': """Day 1: Arrival in Cochin
- Arrive at Cochin International Airport
- Transfer to hotel in Fort Kochi
- Check-in and freshen up
- Evening visit to Fort Kochi
- Watch Chinese Fishing Nets
- Explore Jew Town and Synagogue
- Kathakali dance show
- Dinner at local restaurant
- Overnight stay in Cochin

Day 2: Cochin to Munnar
- Breakfast at hotel
- Check-out and drive to Munnar (130 km, 4 hours)
- En route visit Cheeyappara and Valara waterfalls
- Check-in at Munnar resort
- Lunch at resort
- Evening visit to Tea Gardens
- Tea tasting session
- Dinner at resort
- Overnight stay in Munnar

Day 3: Munnar Sightseeing
- Early breakfast
- Visit Eravikulam National Park (Rajamalai)
- See Nilgiri Tahr (mountain goats)
- Visit Mattupetty Dam and Echo Point
- Lunch at local restaurant
- Visit Tea Museum
- Explore Kundala Lake
- Return to resort
- Dinner and overnight stay

Day 4: Munnar to Alleppey - Houseboat Experience
- Breakfast at resort
- Check-out and drive to Alleppey (170 km, 5 hours)
- Check-in to traditional Kerala houseboat (12:00 PM)
- Welcome drink and lunch on houseboat
- Cruise through backwaters
- Watch village life along the canals
- Sunset on the backwaters
- Dinner on houseboat
- Overnight stay on houseboat

Day 5: Alleppey to Cochin - Departure
- Breakfast on houseboat
- Check-out from houseboat (9:00 AM)
- Drive to Cochin (55 km, 1.5 hours)
- Visit Marine Drive and Lulu Mall for shopping
- Lunch at Cochin
- Transfer to Cochin Airport
- Departure with wonderful memories""",

    'Bali Honeymoon Special': """Day 1: Arrival in Bali
- Arrive at Ngurah Rai International Airport
- Meet and greet with flower garlands
- Private transfer to luxury resort in Ubud
- Welcome drink and check-in
- Romantic room decoration with flowers
- Relax and freshen up
- Couples spa session
- Candlelight dinner at resort
- Overnight stay

Day 2: Ubud Cultural Tour
- Breakfast at resort
- Visit Tegalalang Rice Terraces
- Swing experience at Bali Swing
- Visit Sacred Monkey Forest Sanctuary
- Lunch at restaurant with rice terrace view
- Visit Ubud Royal Palace
- Explore Ubud Art Market
- Traditional Balinese dance performance
- Romantic dinner at resort
- Overnight stay

Day 3: Tanah Lot & Seminyak
- Breakfast at resort
- Check-out and drive to Seminyak
- Visit Tanah Lot Temple - iconic sea temple
- Lunch at beachfront restaurant
- Check-in at beach resort in Seminyak
- Relax at private beach
- Sunset at Seminyak Beach
- Romantic beachside dinner
- Overnight stay

Day 4: Water Sports & Beach Day
- Breakfast at resort
- Visit Tanjung Benoa Beach
- Water sports: Jet ski, parasailing, banana boat
- Lunch at beach club
- Visit Uluwatu Temple on cliff
- Watch Kecak Fire Dance at sunset
- Seafood dinner at Jimbaran Beach
- Overnight stay

Day 5: Nusa Penida Island Tour
- Early breakfast
- Fast boat to Nusa Penida Island
- Visit Kelingking Beach (T-Rex cliff)
- Angel's Billabong natural infinity pool
- Broken Beach
- Packed lunch
- Snorkeling at Crystal Bay
- Return to Bali by evening
- Dinner at resort
- Overnight stay

Day 6: Relaxation & Spa Day
- Breakfast at resort
- Morning at leisure - pool or beach
- Couples massage and spa treatment
- Lunch at resort
- Afternoon shopping at Seminyak boutiques
- Sunset cocktails at beach club
- Farewell romantic dinner
- Overnight stay

Day 7: Departure
- Breakfast at resort
- Check-out
- Last-minute shopping or beach time
- Transfer to airport
- Departure with beautiful memories""",
}

# Update packages
print("Updating package itineraries...")
for title, itinerary in itineraries.items():
    try:
        package = TourPackage.objects.get(title=title)
        package.itinerary = itinerary
        package.save()
        print(f"✓ Updated: {title}")
    except TourPackage.DoesNotExist:
        print(f"✗ Package not found: {title}")

print("\nDone! All itineraries have been updated.")
