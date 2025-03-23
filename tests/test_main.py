import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import geopandas as gpd
from src.main import HOADetectionSystem

class TestHOADetectionSystem(unittest.TestCase):
    @patch('psycopg2.connect')
    def setUp(self, mock_connect):
        # Mock database connection
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor
        
        # Initialize system with test mode
        self.system = HOADetectionSystem()

    @patch('pandas.read_csv')
    def test_analyze_address(self, mock_read_csv):
        """Test single address analysis with proper mock data structure"""
        # Configure mock CSV response
        mock_read_csv.return_value = pd.DataFrame({
            'address': ['1600 Amphitheatre Parkway, Mountain View, CA']
        })
        
        result = self.system.analyze_address("1600 Amphitheatre Parkway, Mountain View, CA")
        self.assertIn("hoa_probability", result)
        self.assertAlmostEqual(result['hoa_probability'], 0.75, places=2)

    @patch('src.main.process_county')
    @patch('pandas.read_csv')
    def test_analyze_county(self, mock_read_csv, mock_process):
        """Test county analysis with mocked CSV reading"""
        # Configure mock CSV response
        mock_read_csv.return_value = pd.DataFrame({
            'address': ['test1', 'test2']
        })
        
        # Configure mock processing response with geometry data
        mock_process.return_value = gpd.GeoDataFrame(
            {
                'address': ['test'],
                'longitude': [0.0],
                'latitude': [0.0],
                'hoa_probability': [0.5]
            },
            geometry=gpd.points_from_xy([0.0], [0.0]),
            crs="EPSG:4326"
        )
        
        result_df = self.system.analyze_county("dummy.csv")
        self.assertIn('geometry', result_df.columns)
        self.assertFalse(result_df.empty)

if __name__ == "__main__":
    unittest.main()
