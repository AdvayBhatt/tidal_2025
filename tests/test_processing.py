import unittest
from unittest.mock import patch
import pandas as pd
from src.geospatial.processing import process_county

class TestProcessCounty(unittest.TestCase):
    @patch('src.main.HOADetectionSystem')  # Corrected import path for HOADetectionSystem mocking
    def test_process_county_with_valid_addresses(self, mock_system):
        """Test processing with valid addresses"""
        
        # Replace MagicMock with concrete data to avoid multiprocessing issues during testing.
        def mock_analyze(address):
            return {
                'address': address,
                'coordinates': (0.0, 0.0),
                'hoa_probability': 0.75,
                'features': {}
            }
        
        mock_instance = mock_system.return_value
        mock_instance.analyze_address.side_effect = mock_analyze
        
        addresses = ["123 Main St"]
        
        results = process_county(addresses)
        
        # Assertions for valid processing behavior.
        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]['hoa_probability'], 0.75)

    def test_process_county_with_empty_list(self):
        """Test processing with empty input"""
        
        results = process_county([])
        
        # Ensure empty input returns an empty DataFrame.
        self.assertTrue(results.empty)

if __name__ == "__main__":
    unittest.main()
