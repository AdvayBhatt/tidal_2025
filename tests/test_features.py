import unittest
from shapely.geometry import Polygon
from src.geospatial.features import HOAFeatureEngineer

class TestHOAFeatureEngineer(unittest.TestCase):
    def setUp(self):
        self.feature_engineer = HOAFeatureEngineer()
    
    def test_calculate_compactness(self):
        polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        compactness = self.feature_engineer.calculate_compactness(polygon)
        expected = (4 * 3.141592653589793 * 1) / (4 ** 2)  # π/4 ≈ 0.785
        self.assertAlmostEqual(compactness, expected, places=2)

    
    def test_calculate_density(self):
        buildings = [{'height': 10}, {'height': 15}]
        density = self.feature_engineer.calculate_density(buildings, parcel_area=10000)
        self.assertEqual(density, 200)  # Buildings per km²

if __name__ == "__main__":
    unittest.main()
