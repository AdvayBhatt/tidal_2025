import geopandas as gpd
from datetime import datetime
import os

def save_for_qgis(gdf: gpd.GeoDataFrame, filename: str):
    """Export GeoDataFrame for QGIS analysis with proper CRS"""
    output_dir = "output/qgis_exports"
    os.makedirs(output_dir, exist_ok=True)
    
    # Ensure consistent CRS for QGIS
    gdf = gdf.to_crs(epsg=4326)
    
    # Save with timestamp
    full_path = f"{output_dir}/{filename}_{datetime.now().strftime('%Y%m%d')}.geojson"
    gdf.to_file(full_path, driver='GeoJSON')
    print(f"Exported {len(gdf)} features to {full_path}")
