import requests

def coordinates(city):
    """
    Get latitude and longitude using Open-Meteo Geocoding API
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params)

    data = response.json()

    if "results" not in data:
        return "Location not found"

    location=data["results"][0]
    
    lat=location["latitude"]
    long=location["longitude"]

    return lat,long
    