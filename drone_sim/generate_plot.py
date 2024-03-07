import requests
import gmplot
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, Point
import random


SAMPLE_COUNT = 100
API_KEY = 'AIzaSyBERVxAAHAu31mUxVmtEoF8KWYhWBfwm3g'

boundary_cords = [(37.75, -122.45),
                   (37.75, -122.35),
                   (37.85, -122.35),
                   (37.85, -122.45),
                   (37.75, -122.45)]
# the boundary cords should be a list of sets


def generate_sample_points(boundary_cords, sample_points):
    """generates the sample points to gather elevation data
    Returns a list of tuples of random points that can be used
    to plot elevation later

    Args:
        boundary_cords (float): a list of tuples of the boundary of map to be plotted
        sample_count (int): the number of sample points to be calculated
    """
    # initalising the polygon to be checked against later if random point in boundary
    boundary_polygon = Polygon(boundary_cords)
    random_points = list()  # to append to later

    while len(random_points) < sample_points:
        # find the maximum and the minimum lat and long
        min_lat, max_lat = min(lat for lat, _ in boundary_cords), max(lat for lat, _ in boundary_cords)
        min_lon, max_lon = min(lon for _, lon in boundary_cords), max(lon for _, lon in boundary_cords)

        # randomly select the lat and long
        rand_lat = random.uniform(min_lat, max_lat)
        rand_lon = random.uniform(min_lon, max_lon)

        # creating the point object
        point = Point(rand_lat, rand_lon)

        # checking if the point is in the specified boundary
        if boundary_polygon.contains(point):
            random_points.append((rand_lat, rand_lon))

    # once done return a list of tuples
    return random_points

def fetch_elevation_data(coordinates, api_key):
    """fetches the elevation data from a google api
    Returns a list of elevation data

    Args:
        coordinates (_type_): _description_
        api_key (_type_): _description_
    """
    base_url = 'https://maps.googleapis.com/maps/api/elevation/json'
    locations = '|'.join(f'{lat},{lng}' for lat, lng in coordinates)
    params = {
        'locations': locations,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    elevations = [result['elevation'] for result in data['results']]

    return elevations


def plot_map(boundary_cords):
    """plots a map of the area simulated

    Args:
        boundary_cords (list): a list containing tuples of the cords data 
    """
    # generate sample points
    sample_points = generate_sample_points(boundary_cords, SAMPLE_COUNT)
    # generate the eleveation data
    elevations = fetch_elevation_data(sample_points, API_KEY)
    # generating lat and lon data
    latitudes, longitudes = boundary_cords[:, 0], boundary_cords[:, 1]
    # reshaping elevation data
    z = np.array(elevations).reshape(SAMPLE_COUNT, 1)

    # plotting the map
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(latitudes, longitudes, z, c=z, cmap='terrain')
    ax.set_title('Non-Uniform Elevation Map')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Elevation (m)')
    plt.show()
    
plot_map(boundary_cords)