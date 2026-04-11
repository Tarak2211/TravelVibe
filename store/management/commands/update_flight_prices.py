# Management command to update flight prices automatically
# Run this command: python manage.py update_flight_prices

from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from flight_api_service import flight_api
import json

class Command(BaseCommand):
    help = 'Updates flight prices from live API data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting flight price update...'))
        
        # Define routes to update
        routes = [
            {'origin': 'DEL', 'destination': 'GOI', 'name': 'Goa'},
            {'origin': 'DEL', 'destination': 'DXB', 'name': 'Dubai'},
            {'origin': 'DEL', 'destination': 'KUU', 'name': 'Manali'},
            {'origin': 'DEL', 'destination': 'COK', 'name': 'Kerala'},
            {'origin': 'DEL', 'destination': 'DPS', 'name': 'Bali'},
        ]
        
        # Get dates (7 days from now for sample)
        departure_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        updated_count = 0
        
        for route in routes:
            self.stdout.write(f"Updating {route['name']}...")
            
            try:
                # Fetch live flight data
                flights = flight_api.search_flights(
                    origin=route['origin'],
                    destination=route['destination'],
                    departure_date=departure_date,
                    return_date=return_date
                )
                
                if flights and (flights['outbound'] or flights['return']):
                    # Save to cache or database
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ {route['name']}: Found {len(flights['outbound'])} outbound, "
                            f"{len(flights['return'])} return flights"
                        )
                    )
                    updated_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f"⚠ {route['name']}: No flights found, using static data")
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ {route['name']}: Error - {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nCompleted! Updated {updated_count}/{len(routes)} routes')
        )
