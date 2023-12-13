import requests

url = "https://data.veridion.com/match/v4/companies"

headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, headers=headers)

print(response.text)

def veridion(lat, long, name, adrs):
    return str_json