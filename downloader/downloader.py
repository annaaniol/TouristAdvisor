import requests
import numpy as np
from geopy.geocoders import Nominatim


class Downloader:
    def __init__(self, city_name):
        self.api_key = "ca830d075b22ef03d4556f9405fa17ad"
        self.city_name = city_name
        self.city_location = ""
        self.points_location = []
        self.photo_ids = []
        self.coordinates = []

    def get_city_coordinates(self):
        geolocator = Nominatim()
        self.city_location = geolocator.geocode(self.city_name)

    def get_photo_ids(self, latitude, longitude):
        URL = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}" \
              "&accuracy=11&has_geo&lat={1}&lon={2}&format=json&nojsoncallback=1".\
            format(self.api_key, self.city_location.latitude, self.city_location.longitude)
        Response = requests.get(URL).json()

        for photos in Response['photos']['photo']:
            self.photo_ids.append(photos['id'])

    def get_locations(self):
        for ID in self.photo_ids:
            URL = "https://api.flickr.com/services/rest/?method=flickr.photos.geo.getLocation" \
                  "&api_key={0}&photo_id={1}&format=json&nojsoncallback=1".format(self.api_key, ID)
            Response = requests.get(URL).json()
            lat = Response['photo']['location']['latitude']
            lon = Response['photo']['location']['longitude']
            self.coordinates.append((lat, lon))

    def write_to_csv(self):
        for cord_tuple in self.coordinates:
            print (cord_tuple[0] + "," + cord_tuple[1])

    def get_points(self):
        self.get_city_coordinates()
        self.get_photo_ids(self.city_location.latitude, self.city_location.longitude)
        self.get_locations()
        self.write_to_csv()


downloader = Downloader("Krakow")
downloader.get_points()
