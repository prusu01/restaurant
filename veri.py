import requests


def version_match_and_enrich(api_key, restaurant_name, coordinates):
    url = "https://data.veridion.com/match/v4/companies"

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    response = requests.post(base_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
    return response.json()        


# Example usage:
api_key = 'Lk34BnMBMFDj07xGbkQ_aNikeD4_NSKq643WxEEuQUAcjtbrVJStX9FpASw7'
restaurant_name = 'Example Restaurant'
coordinates = {'latitude': 37.7749, 'longitude': -122.4194}

result = version_match_and_enrich(api_key, restaurant_name, coordinates)
print(result)
