import requests

place = 'Podanur'
url = "https://api.geoapify.com/v1/geocode/search?text=" + place + "&format=json&apiKey=67f3b4876f964d49a0bfc8150d784964"

response = requests.get(url)

output = response.json()
lat1 =  output['results'][0]['lat']
lon1 =  output['results'][0]['lon']

place = 'Ramanathapuram'
url = "https://api.geoapify.com/v1/geocode/search?text=" + place + "&format=json&apiKey=67f3b4876f964d49a0bfc8150d784964"

response = requests.get(url)

output = response.json()
lat2 =  output['results'][0]['lat']
lon2 =  output['results'][0]['lon']

url = f"https://api.geoapify.com/v1/routing?waypoints={lat1},{lon1}|{lat2},{lon2}&mode=drive&apiKey=67f3b4876f964d49a0bfc8150d784964"
response = requests.get(url)
output = response.json()

dist = output['features'][0]['properties']['distance']
unit = output['features'][0]['properties']['distance_units']
print(dist, unit)
