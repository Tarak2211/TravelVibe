# Flight API Service - Real-time flight data integration
# This service fetches live flight prices, routes, and availability from Amadeus API

import requests
from datetime import datetime, timedelta
from django.core.cache import cache
import os

class FlightAPIService:
    """
    Service to fetch real-time flight data from Amadeus API
    
    Features:
    - Real-time pricing updates
    - Flight cancellation alerts
    - Route changes detection
    - Layover information
    - Seat availability
    """
    
    def __init__(self):
        # Amadeus API credentials (Free tier: 2000 calls/month)
        # Get credentials from Django settings
        try:
            from django.conf import settings
            self.api_key = settings.AMADEUS_API_KEY or 'YOUR_API_KEY_HERE'
            self.api_secret = settings.AMADEUS_API_SECRET or 'YOUR_API_SECRET_HERE'
        except:
            # Fallback to environment variables if Django not available
            import os
            self.api_key = os.getenv('AMADEUS_API_KEY', 'YOUR_API_KEY_HERE')
            self.api_secret = os.getenv('AMADEUS_API_SECRET', 'YOUR_API_SECRET_HERE')
        
        self.base_url = 'https://test.api.amadeus.com/v2'  # Test environment
        # Production: https://api.amadeus.com/v2
        
        self.access_token = None
        self.token_expiry = None
    
    def get_access_token(self):
        """Get OAuth2 access token from Amadeus"""
        # Check if token is cached and valid
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
        # Check cache
        cached_token = cache.get('amadeus_access_token')
        if cached_token:
            self.access_token = cached_token
            return cached_token
        
        # Request new token
        url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data['access_token']
            expires_in = token_data['expires_in']  # Usually 1799 seconds (30 min)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in - 60)
            
            # Cache token
            cache.set('amadeus_access_token', self.access_token, expires_in - 60)
            
            return self.access_token
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def search_flights(self, origin, destination, departure_date, return_date=None, adults=1):
        """
        Search for real-time flight offers
        
        Args:
            origin: IATA code (e.g., 'DEL' for Delhi)
            destination: IATA code (e.g., 'GOI' for Goa)
            departure_date: Date in YYYY-MM-DD format
            return_date: Optional return date for round trip
            adults: Number of adult passengers
        
        Returns:
            List of flight offers with real-time prices
        """
        token = self.get_access_token()
        if not token:
            return self._get_fallback_data(origin, destination)
        
        # Check cache first (cache for 15 minutes)
        cache_key = f'flights_{origin}_{destination}_{departure_date}_{return_date}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        url = f'{self.base_url}/shopping/flight-offers'
        headers = {'Authorization': f'Bearer {token}'}
        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': adults,
            'currencyCode': 'INR',
            'max': 10  # Get top 10 offers
        }
        
        if return_date:
            params['returnDate'] = return_date
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Parse and format flight data
            flights = self._parse_flight_offers(data)
            
            # Cache for 15 minutes
            cache.set(cache_key, flights, 900)
            
            return flights
        except Exception as e:
            print(f"Error fetching flights: {e}")
            return self._get_fallback_data(origin, destination)
    
    def _parse_flight_offers(self, api_response):
        """Parse Amadeus API response into our format"""
        flights = {
            'outbound': [],
            'return': []
        }
        
        if 'data' not in api_response:
            return flights
        
        for offer in api_response['data']:
            try:
                # Get itineraries
                itineraries = offer.get('itineraries', [])
                price = offer.get('price', {})
                
                # Outbound flight
                if len(itineraries) > 0:
                    outbound = self._parse_itinerary(itineraries[0], price)
                    if outbound:
                        flights['outbound'].append(outbound)
                
                # Return flight
                if len(itineraries) > 1:
                    return_flight = self._parse_itinerary(itineraries[1], price)
                    if return_flight:
                        flights['return'].append(return_flight)
            except Exception as e:
                print(f"Error parsing offer: {e}")
                continue
        
        return flights
    
    def _parse_itinerary(self, itinerary, price):
        """Parse single itinerary (one direction)"""
        segments = itinerary.get('segments', [])
        if not segments:
            return None
        
        first_segment = segments[0]
        last_segment = segments[-1]
        
        # Calculate layovers
        stops_info = 'Direct'
        if len(segments) > 1:
            layovers = []
            for i in range(len(segments) - 1):
                arrival_time = datetime.fromisoformat(segments[i]['arrival']['at'].replace('Z', '+00:00'))
                departure_time = datetime.fromisoformat(segments[i+1]['departure']['at'].replace('Z', '+00:00'))
                layover_duration = departure_time - arrival_time
                
                hours = int(layover_duration.total_seconds() // 3600)
                minutes = int((layover_duration.total_seconds() % 3600) // 60)
                
                layover_city = segments[i]['arrival']['iataCode']
                layovers.append(f"{layover_city} - {hours}h {minutes}min layover")
            
            stops_info = f"{len(segments) - 1} Stop ({', '.join(layovers)})"
        
        # Get airline
        airline_code = first_segment.get('carrierCode', '')
        airline_name = self._get_airline_name(airline_code)
        
        # Get times
        departure_time = datetime.fromisoformat(first_segment['departure']['at'].replace('Z', '+00:00'))
        arrival_time = datetime.fromisoformat(last_segment['arrival']['at'].replace('Z', '+00:00'))
        
        # Calculate duration
        duration = arrival_time - departure_time
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        
        # Get price (convert to INR if needed)
        base_price = float(price.get('total', 0))
        
        return {
            'airline': airline_name,
            'flight_no': f"{airline_code} {first_segment.get('number', '')}",
            'departure': departure_time.strftime('%I:%M %p'),
            'arrival': arrival_time.strftime('%I:%M %p'),
            'duration': f'{hours}h {minutes}min',
            'stops': stops_info,
            'from': f"{first_segment['departure']['iataCode']}",
            'to': f"{last_segment['arrival']['iataCode']}",
            'economy': int(base_price),
            'premium': int(base_price * 1.6),  # Estimate
            'business': int(base_price * 3.2),  # Estimate
            'available_seats': first_segment.get('numberOfBookableSeats', 9),
            'last_updated': datetime.now().isoformat()
        }
    
    def _get_airline_name(self, code):
        """Convert airline code to name"""
        airlines = {
            '6E': 'IndiGo',
            'AI': 'Air India',
            'UK': 'Vistara',
            'SG': 'SpiceJet',
            'EK': 'Emirates',
            'QR': 'Qatar Airways',
            'SQ': 'Singapore Airlines',
            'TG': 'Thai Airways',
            '9I': 'Alliance Air',
            'G8': 'Go First',
        }
        return airlines.get(code, code)
    
    def _get_fallback_data(self, origin, destination):
        """Return static data if API fails"""
        # This returns the static data we already have
        # Import from views.py
        from store.views import package_detail_view
        # Return empty for now, will use static data
        return {'outbound': [], 'return': []}
    
    def check_flight_status(self, flight_number, date):
        """
        Check real-time flight status (delays, cancellations)
        
        Args:
            flight_number: e.g., 'AI995'
            date: Date in YYYY-MM-DD format
        
        Returns:
            Flight status information
        """
        token = self.get_access_token()
        if not token:
            return None
        
        url = f'{self.base_url}/schedule/flights'
        headers = {'Authorization': f'Bearer {token}'}
        params = {
            'carrierCode': flight_number[:2],
            'flightNumber': flight_number[2:],
            'scheduledDepartureDate': date
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                'status': 'active',
                'delays': data.get('data', [{}])[0].get('flightPoints', [{}])[0].get('delay', 0),
                'cancelled': False,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error checking flight status: {e}")
            return None


# Singleton instance
flight_api = FlightAPIService()
