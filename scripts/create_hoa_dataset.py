import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
from src.geospatial.features import calculate_compactness

def create_hoa_dataset():
    # Load county parcel data
    parcels = gpd.read_file("data/raw/denton_county_parcels.shp")
    
    # Load Bing building footprints
    buildings = gpd.read_file("data/raw/bing_building_footprints.geojson")
    
    # Load National Address Database
    nad = pd.read_csv("data/raw/national_address_database.csv")
    
    def process_parcel(parcel):
        # Calculate compactness
        compactness = calculate_compactness(parcel.geometry)
        
        # Check for common areas (pools, parks)
        parcel_buildings = buildings[buildings.within(parcel.geometry)]
        has_pool = any(b for b in parcel_buildings if b['type'] == 'pool')
        has_park = any(b for b in parcel_buildings if b['type'] == 'park')
        
        # Calculate building density
        building_density = len(parcel_buildings) / parcel.geometry.area
        
        # Check for clustered addresses
        parcel_addresses = nad[(nad['latitude'].between(parcel.geometry.bounds[1], parcel.geometry.bounds[3])) & 
                               (nad['longitude'].between(parcel.geometry.bounds[0], parcel.geometry.bounds[2]))]
        address_density = len(parcel_addresses) / parcel.geometry.area
        
        # Roof consistency (assuming 'roof_type' is a feature in building footprints)
        roof_types = set(b['roof_type'] for b in parcel_buildings if 'roof_type' in b)
        roof_consistency = 1 - (len(roof_types) / len(parcel_buildings) if len(parcel_buildings) > 0 else 0)
        
        return {
            'parcel_id': parcel.id,
            'compactness': compactness,
            'has_pool': has_pool,
            'has_park': has_park,
            'building_density': building_density,
            'address_density': address_density,
            'roof_consistency': roof_consistency,
            # You would need to determine this based on your knowledge or additional data
            'hoa_exists': None  # This will need to be filled in later
        }
    
    hoa_data = parcels.apply(process_parcel, axis=1)
    
    return pd.DataFrame(hoa_data.tolist())

if __name__ == "__main__":
    hoa_dataset = create_hoa_dataset()
    hoa_dataset.to_csv("data/processed/hoa_features.csv", index=False)