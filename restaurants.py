import requests

def get_nearby_restaurants(api_key, latitude, longitude, radius=500, keyword='restaurant'):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Set up parameters for the API request
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'keyword': keyword,
        'key': api_key
    }

    # Make the API request
    response = requests.get(endpoint_url, params=params)
    results = response.json().get('results', [])

    # Print information about nearby restaurants
    for place in results:
        name = place.get('name', 'N/A')
        address = place.get('vicinity', 'N/A')
        rating = place.get('rating', 'N/A')
        price_level = place.get('price_level', 'N/A')
        price_mapping = {0: 'Free', 1: 'Inexpensive', 2: 'Moderate', 3: 'Expensive', 4: 'Very Expensive'}
        price_range = price_mapping.get(price_level, 'N/A')
        print(f"Name: {name}, Address: {address}, Rating: {rating}, Price Range: {price_range}")

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'AIzaSyCRuJ_aBmW-QqYPrVTY4hjDbZ8_DspaLZM'
    
    # Input coordinates (latitude and longitude)
    input_latitude = 44.4751797
    input_longitude = 26.0813026

    # Call the function to get nearby restaurants
    get_nearby_restaurants(api_key, input_latitude, input_longitude)
