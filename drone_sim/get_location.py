import requests
import random
from shapely.geometry import Polygon, Point
from geopy.distance import geodesic



def get_coordinates(address):
    """generates the lat and lon points of a given address to serve as the 
    center of the map generated

    Args:
        address (string): the address used to provide the optical center of
        the map

    Returns:
        tuple: lat, lon of the location from google maps api
    """
    api_key = "AIzaSyBD1V7xVVhTTjNFXyXeIPxuxplQPT-jDuE"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        print("Error:", data['status'])
        return None, None

def generate_random_area(center_lat,center_lon, rad, points):
    points = list()
    
    # convert lat and lon to point
    num_points = random.randint(points/2, points)

    # iterate to get the number of points required
    for _ in range(points):
        bearing = random.randint(0, 360)
        distance = random.uniform(rad, )
    


address = "1600 Amphitheatre Parkway, Mountain View, CA"  # Example address
latitude, longitude = get_coordinates(address)
if latitude is not None and longitude is not None:
    print("Latitude:", latitude)
    print("Longitude:", longitude)