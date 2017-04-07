import requests
import sys
from geopy.geocoders import Nominatim

api_key = "ca830d075b22ef03d4556f9405fa17ad"
city = sys.argv[1]

def getCoordinates(city):
    geolocator = Nominatim()
    location = geolocator.geocode(city)
    print('Found city: '+location.address)
    return (location.latitude, location.longitude)

def getPhotoIDs(lat, lon):
    URL = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}" \
          "&accuracy=11&has_geo&lat={1}&lon={2}&format=json&nojsoncallback=1".format(api_key, lat, lon)
    Response = requests.get(URL).json()
    PhotoIDs = []

    for photos in Response['photos']['photo']:
        PhotoIDs.append(photos['id'])
    return PhotoIDs

def getLocations(IDs):
    f = open('location_data','w')
    Locations = []

    for ID in IDs:
        URL = "https://api.flickr.com/services/rest/?method=flickr.photos.geo.getLocation" \
              "&api_key=ca830d075b22ef03d4556f9405fa17ad&photo_id={0}&format=json&nojsoncallback=1".format(ID)
        Response = requests.get(URL).json()
        lat = Response['photo']['location']['latitude']
        lon = Response['photo']['location']['longitude']
        f.write(lat+' '+lon+'\n')
        Locations.append((lat,lon))
        print(lat+' '+lon)

    f.close()
    return Locations


(latitude,longitude) = getCoordinates(city)
PhotoIDs = getPhotoIDs(latitude, longitude)
Locations = getLocations(PhotoIDs)


