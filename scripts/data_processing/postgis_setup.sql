CREATE EXTENSION postgis;
CREATE TABLE parcels (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Polygon, 4326),
    address TEXT,
    zoning_type VARCHAR(50),
    land_use_code VARCHAR(10)
);

CREATE TABLE bing_buildings (
    building_id BIGINT PRIMARY KEY,
    geom GEOMETRY(Polygon, 4326),
    height FLOAT,
    confidence FLOAT
);
