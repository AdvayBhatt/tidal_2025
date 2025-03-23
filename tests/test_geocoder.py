import unittest
from unittest.mock import patch, Mock
from src.geospatial.geocoder import EnhancedGeocoder

class TestEnhancedGeocoder(unittest.TestCase):
    @patch('src.geospatial.geocoder.GoogleV3')
    def setUp(self, mock_google):
        # Mock GoogleV3 instance and its methods
        self.mock_geocoder = mock_google.return_value
        self.geocoder = EnhancedGeocoder()  # Now uses env var/keychain

    def test_geocode_valid_address(self):
        # Configure mock response
        self.mock_geocoder.geocode.return_value = Mock(
            latitude=37.423021,
            longitude=-122.083739
        )
        
        result = self.geocoder.geocode("1600 Amphitheatre Parkway, Mountain View, CA")
        self.assertEqual(result, (37.423021, -122.083739))
        self.mock_geocoder.geocode.assert_called_once_with("1600 Amphitheatre Parkway, Mountain View, CA")

    def test_geocode_invalid_address(self):
        # Configure mock failure
        self.mock_geocoder.geocode.return_value = None
        
        result = self.geocoder.geocode("Invalid Address")
        self.assertEqual(result, (None, None))
        self.mock_geocoder.geocode.assert_called_once_with("Invalid Address")

if __name__ == "__main__":
    unittest.main()
