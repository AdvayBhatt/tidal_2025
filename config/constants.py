import os
# Spatial analysis parameters
BUFFER_RADIUS = 100  # meters
COMPACTNESS_THRESHOLD = 0.6
DENSITY_THRESHOLD = 20  # buildings/km²

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'hoa_detection',
    'user': 'postgres',
    'password': os.getenv('DB_PASSWORD'),
    'port': 5432
}