import requests, json

# base_url variable to store url
base_url = "https://api.weather.gov/points/40.90243696271137,-74.0344921768194"

response = requests.get(base_url)

x = response.json()

forecast_url = x['properties']['forecast']
print(forecast_url)

r = requests.get(forecast_url)
forecast = r.json()
print(forecast['properties']['periods'][0]['temperature'])
print(forecast['properties']['periods'][1]['temperature'])

