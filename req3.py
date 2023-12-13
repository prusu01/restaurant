import requests

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

#veridon goes here

def get_specific(name, adress, lat, long):
    str=veridon(name, address, lat, long)

    all_specialties=[]

    for specialty in all_restaurant_types:
        if specialty in str:
            all_specialties.append(specialty)
    
    return all_specialties


    
    #find given restaurant in veridon, return all the strings that match with specificsm return list of strings


def count_transit_stations(api_key, latitude, longitude, radius=500, type='transit_station'):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Set up parameters for the Places API request
    transit_params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': type,
        'key': api_key
    }

    # Make the Places API request
    transit_response = requests.get(endpoint_url, params=transit_params)
    transit_results = transit_response.json().get('results', [])

    all_stations = [];
    for station in transit_results:
        station_info = {
            'name': station.get('name', 'N/A'),
            'address': station.get('vicinity', 'N/A'),
        }

    all_stations.append(station_info)

    # Count the number of transit stations
    return all_stations

def get_nearby_restaurants(api_key, latitude, longitude, radius=500, keyword='restaurant'):
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

    # List to store information about all restaurants
    all_restaurants = []

    #nm = place.get('name', 'N/A')
    #adr = place.get('vicinity', 'N/A')

    # Process each restaurant and save relevant information
    for place in places_results:
        restaurant_info = {
            'name': place.get('name', 'N/A'),
            'address': place.get('vicinity', 'N/A'),
            'rating': place.get('rating', 'N/A'),
            'price_level': place.get('price_level', 'N/A'),
            'latitude': place['geometry']['location']['lat'],
            'longitude': place['geometry']['location']['lng'],
            'types': place.get('types', []),
            'transit_count': count_transit_stations(api_key, place['geometry']['location']['lat'], place['geometry']['location']['lng']),
            'specifics': get_specific('name', 'address', latitude, longitude)
        }

        # Map price level to a more human-readable format
        price_mapping = {0: 'Free', 1: 'Inexpensive', 2: 'Moderate', 3: 'Expensive', 4: 'Very Expensive'}
        restaurant_info['price_range'] = price_mapping.get(restaurant_info['price_level'], 'N/A')

        # Add the restaurant information to the list
        all_restaurants.append(restaurant_info)

    return all_restaurants


def model(restaurants, stations, specific, location, price):
    ans=0
    for rest in restaurants:
        ans=ans+restaurants['rating']/5*((4-abs(price-rest['price_range'])))


if __name__ == "__main__":
    api_key = "AIzaSyCRuJ_aBmW-QqYPrVTY4hjDbZ8_DspaLZM"
    location=input("Where would you like to open a restaurant? ")
    address = location + " Bucuresti, Romania"

    # Geocoding API endpoint
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"

    # Make the request
    response = requests.get(url)
    data = response.json()

    # Parse the response
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
    else:
        print("Error:", data['status'])

    nearby_restaurants = get_nearby_restaurants(api_key, location['lat'], location['lng'])

    # Print the information about all restaurants
    for idx, restaurant in enumerate(nearby_restaurants, 1):
        print(f"\nRestaurant {idx}:")
        print(f"Name: {restaurant['name']}")
        print(f"Address: {restaurant['address']}")
        print(f"Rating: {restaurant['rating']}")
        print(f"Price Range: {restaurant['price_range']}")
        print(f"Latitude: {restaurant['latitude']}")
        print(f"Longitude: {restaurant['longitude']}")
        print(f"Types: {', '.join(restaurant['types'])}")
        #print(f"transit_count: {restaurant['transit_count']}")

    nearby_stations = count_transit_stations(api_key, location['lat'], location['lng'])

    for idx, station in enumerate(nearby_stations, 1):
        print(f"\nStation {idx}:")
        print(f"Name: {station['name']}")
        print(f"Adresa: {station['address']}")

    my_specific=input("ce specific vrei? ")
    my_price=input("ce pret range vrei? ")

    score=model(nearby_restaurants, nearby_stations, my_specific, location, my_price)

    #print(count_transit_stations(api_key, location['lat'], location['lng']))