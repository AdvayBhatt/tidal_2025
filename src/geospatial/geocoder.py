import os
from dotenv import load_dotenv
from geopy.geocoders import GoogleV3

load_dotenv()

class EnhancedGeocoder:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key not found")
        self.geolocator = GoogleV3(api_key=self.api_key)

    def geocode(self, address: str):
        location = self.geolocator.geocode(address)
        return (location.latitude, location.longitude) if location else (None, None)