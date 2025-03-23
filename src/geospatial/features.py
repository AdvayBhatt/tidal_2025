from shapely.geometry import shape, Polygon
import numpy as np

class HOAFeatureEngineer:
    def __init__(self):
        pass

    def calculate_compactness(self, polygon: Polygon) -> float:
        """Calculate compactness of a polygon."""
        area = polygon.area
        perimeter = polygon.length
        return (4 * np.pi * area) / (perimeter ** 2)

    def calculate_density(self, buildings: list, parcel_area: float) -> float:
        """Calculate building density (buildings per square kilometer)."""
        return len(buildings) / (parcel_area / 1e6)  # Convert m² to km²

    def combine_features(self, parcel: dict, buildings: list) -> dict:
        """Combine spatial features into a single dictionary."""
        parcel_geom = shape(parcel['geometry'])
        compactness = self.calculate_compactness(parcel_geom)
        
        # Assume parcel['area'] is in square meters
        density = self.calculate_density(buildings, parcel['area'])
        
        # Calculate height variation if building heights are available
        heights = [b['height'] for b in buildings if 'height' in b]
        height_variation = np.std(heights) if heights else 0
        
        return {
            'compactness': compactness,
            'density': density,
            'height_variation': height_variation,
            'zoning_code': parcel.get('zoning', None),
            'land_use': parcel.get('land_use', None)
        }
