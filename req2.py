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

# Combine all types into a single list
all_restaurant_types = restaurant_types + cuisine_types + specific_food_types + meal_types + specialty_types

print(all_restaurant_types)

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

    # Count the number of transit stations
    transit_count = len(transit_results)

    return transit_count

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

    # Count transit stations for each restaurant and categorize the region
    for place in places_results:
        name = place.get('name', 'N/A')
        address = place.get('vicinity', 'N/A')
        rating = place.get('rating', 'N/A')
        price_level = place.get('price_level', 'N/A')

        # Map price level to a more human-readable format
        price_mapping = {0: 'Free', 1: 'Inexpensive', 2: 'Moderate', 3: 'Expensive', 4: 'Very Expensive'}
        price_range = price_mapping.get(price_level, 'N/A')

        # Count transit stations for the region
        transit_count = count_transit_stations(api_key, place['geometry']['location']['lat'], place['geometry']['location']['lng'])

        # Categorize the region based on the number of transit stations
        if transit_count >= 3:
            region_type = 'Busy'
        elif transit_count >= 1:
            region_type = 'Moderate'
        else:
            region_type = 'Quiet'

        print(f"Name: {name}, Address: {address}, Rating: {rating}, Price Range: {price_range}, Region Type: {transit_count}")

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

    get_nearby_restaurants(api_key, location['lat'], location['lng'])

