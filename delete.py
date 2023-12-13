#!/usr/bin/env python
import requests
import google_maps
import match_types

class Veridion:
    def __init__(self, api_key, address, name, maps_key):
        self.api_key = api_key
        self.address = address
        self.name = name
        self.maps_key = maps_key
    
    def request(self, lat, long):
        url = 'https://data.veridion.com/match/v4/companies'
        headers = {
            'x-api-key': self.api_key,  
            'Content-type': 'application/json'
        }
        data = {
            "legal_names": [self.name],  # Change to a list
            "address_txt": self.address,  # Change to a list
            "locations_latitude": lat,
            "locations_longitude": long  # Corrected typo
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return str(result)
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def veridion(self):
        coord = google_maps.Maps(self.address, self.maps_key,self.api_key) 
        lat, long = coord.get_lat_long()
        self.request(lat, long)

    def get_specific(self):
        restaurant_types = [
        'restaurant',
        'bar',
        'cafe',
        'night_club',
        'pub',
        'bakery',
        'meal_delivery',
        'meal_takeaway',
        'liquor_store',
        'grocery_or_supermarket',
        'convenience_store',
        'food',
        'store',
        'shopping_mall',
        'department_store',
        'supermarket',
        'gas_station',
        'pharmacy',
        'book_store'
        ]

        cuisine_types = [
            'chinese',
            'japanese',
            'indian',
            'italian',
            'mexican',
            'thai',
            'french',
            'greek',
            'spanish',
            'american',
            'korean',
            'vietnamese',
            'mediterranean',
            'middle_eastern',
            'turkish',
            'brazilian',
            'peruvian',
            'argentinian',
            'moroccan',
            'caribbean',
            'african',
            'hawaiian',
            'filipino',
            'asian',
            'latin_american',
            'cuban',
            'russian',
            'german',
            'irish',
            'british',
            'australian',
            'canadian'
            ]

        specific_food_types = [
            'pizza',
            'sushi',
            'burger',
            'sandwich',
            'ice_cream',
            'donut',
            'bakery',
            'coffee_shop',
            'juice_bar',
            'smoothie',
            'tea',
            'ramen',
            'noodle',
            'hot_dog',
            'frozen_yogurt'
            ]

        meal_types = [
            'breakfast',
            'brunch',
            'lunch',
            'dinner'
            ]

        specialty_types = [
            'seafood',
            'steakhouse',
            'vegetarian',
            'vegan',
            'gluten_free',
            'organic',
            'farmers_market'
            ]
        all_restaurant_types = restaurant_types + cuisine_types + specific_food_types + meal_types + specialty_types
        str = self.veridion()
        all_specialties=[]
        for specialty in all_restaurant_types:
            if specialty in str:
                all_specialties.append(specialty)
        
        return all_specialties