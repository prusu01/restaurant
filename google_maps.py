
#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

class Maps:
    def __init__(self,address,api_key):
        self.location=address
        self.api_key=api_key
    
    def get_lat_long(self):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={self.location}&key={self.api_key}"
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'OK':
             location = data['results'][0]['geometry']['location']
             return location['lat'], location['lng']
        else:
             print("Error:", data['status'])

        return None, None
    

    def get_info(self):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={self.location}&key={self.api_key}"
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'OK':
             location = data['results'][0]['geometry']['location']
        else:
             print("Error:", data['status'])
        self.get_nearby_restaurants(self.api_key, location['lat'], location['lng'])
    
    def get_nearby_restaurants(self,api_key, latitude, longitude, radius=500, keyword='restaurant'):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        # Set up parameters for the Places API request
        places_params = {
            'location': f'{latitude},{longitude}',
            'radius': radius,
            'keyword': keyword,
            'key': api_key
        }

        # Make the Places API request
        places_response = requests.get(endpoint_url, params=places_params)
        places_results = places_response.json().get('results', [])

        # Print information about nearby restaurants
        for place in places_results:
            name = place.get('name', 'N/A')
            address = place.get('vicinity', 'N/A')
            rating = place.get('rating', 'N/A')
            price_level = place.get('price_level', 'N/A')
            place_id = place.get('place_id', 'N/A')

            # Map price level to a more human-readable format
            price_mapping = {0: 'Free', 1: 'Inexpensive', 2: 'Moderate', 3: 'Expensive', 4: 'Very Expensive'}
            price_range = price_mapping.get(price_level, 'N/A')

            print(f"Name: {name}, Address: {address}, Rating: {rating}, Price Range: {price_range}")