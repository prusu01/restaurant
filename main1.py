import requests
from unidecode import unidecode
import subprocess
veridion_key="Lk34BnMBMFDj07xGbkQ_aNikeD4_NSKq643WxEEuQUAcjtbrVJStX9FpASw7"
restaurant_types = [
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

def veridion(commercial_names, address_txt, locations_latitude, locations_longitude):
    url = "https://data.veridion.com/match/v4/companies"

    data = {
        "commercial_names": [commercial_names],
        "address_txt": address_txt,
        "locations_latitude": locations_latitude,
        "locations_longitude": locations_longitude
    }

    headers = {
        "x-api-key": "Lk34BnMBMFDj07xGbkQ_aNikeD4_NSKq643WxEEuQUAcjtbrVJStX9FpASw7",
        "Content-type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    return response.text


def get_specific(name, address, lat, long):
    result_str = veridion(name, address, lat, long)
    
    all_specialties=[]

    for specialty in all_restaurant_types:
        if specialty.lower() in result_str.lower():
            all_specialties.append(specialty.lower())

    return all_specialties
    
    #find given restaurant in veridon, return all the strings that match with specificsm return list of strings


def count_transit_stations(api_key, latitude, longitude, radius=750, type='transit_station'):
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

    all_stations = []
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
            'name': place.get('name', '1'),
            'address': place.get('vicinity', '1'),
            'rating': place.get('rating', 'N/A'),
            'price_level': place.get('price_level', '1'),
            'latitude': place['geometry']['location']['lat'],
            'longitude': place['geometry']['location']['lng'],
            'types': place.get('types', []),
            'transit_count': count_transit_stations(api_key, place['geometry']['location']['lat'], place['geometry']['location']['lng']),
            'specifics': get_specific(place.get('name', '1'), place.get('vicinity', '1'), latitude, longitude)
        }

        # Map price level to a more human-readable format
        #price_mapping = {0: 'Free', 1: 'Inexpensive', 2: 'Moderate', 3: 'Expensive', 4: 'Very Expensive'}
        #restaurant_info['price_range'] = price_mapping.get(restaurant_info['price_level'], 'N/A')

        # Add the restaurant information to the list
        all_restaurants.append(restaurant_info)

    return all_restaurants


def model(restaurants, number, specific, location, price):
    ans=int(0)
    c1=float(0.4)
    c2=float(0.2)
    c3=float(0.4)
    c4=float(1)
    c5=int(1)
    issame=(int)(0)
    rating_avg=(int)(0)
    #if specific in restaurants['specifics']:
    issame=1
    for rest in restaurants:
        if specific in rest['specifics']:
            issame=0
        ans=(int)(ans)+(max ((int)(rest['rating']) - 2 , 0) )/3*( c1*((4-abs((int)(price)-(int)(rest['price_level'])))/4) + 
                                         c2*issame + c3*min(12, (int)(number))/12)
        rating_avg=rating_avg+(int)(rest['rating'])
        issame=1
    

    if((int)(len(restaurants))==0):
        print("We don't have enough information to decide")
        return -1
    
    rating_avg=rating_avg/(len(restaurants)-1)
    ans=ans*c4
    ans = ans/len(restaurants)
    ans=ans+c5*(1-rating_avg/5)
    return ans




if __name__ == "__main__":
    api_key = "AIzaSyCRuJ_aBmW-QqYPrVTY4hjDbZ8_DspaLZM"
    print("Where would you like to open a restaurant? ")
    address = input("Type the input in this form: <zone> <city>, <country> ")
    my_specific = input("What's your restaurant specific? ")
    my_price = input("What's your price range for the menu (0-4)? ")
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
        print(f"Price LEVEL: {restaurant['price_level']}")
        print(f"Latitude: {restaurant['latitude']}")
        print(f"Longitude: {restaurant['longitude']}")
        print(f"Types: {', '.join(restaurant['types'])}")
        print(f"Specific: {restaurant['specifics']}")
        #print(f"transit_count: {restaurant['transit_count']}")

    nearby_stations = count_transit_stations(api_key, location['lat'], location['lng'])
    """
    for idx, station in enumerate(nearby_stations, 1):
        print(f"\nStation {idx}:")
        print(f"Name: {station['name']}")
        print(f"Adresa: {station['address']}")
    """
    


    score=model(nearby_restaurants, len(nearby_stations) , my_specific, location, my_price)
    if ((int)(score)!=-1):
        print("\n\nYour chance of succeding is: ")
        print(score*100,end="")
        print("%")
    #print(count_transit_stations(api_key, location['lat'], location['lng']))