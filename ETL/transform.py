import pandas as pd 
from math import radians, sin, cos, sqrt, asin


def transform_house_data(house_prices):
    houses_clean = house_prices[[
        "listing_id",
        "price",
        "district",
        "neighborhood",
        "rooms",
        "gross_sqm",
        "net_sqm",
        "building_age",
        "floor",
        "total_floors",
        "bathroom_count",
        "price_per_sqm"
    ]].copy()
    
    houses_clean['floor'] = houses_clean['floor'].fillna(houses_clean['floor'].median())
    houses_clean["total_floors"] = houses_clean["total_floors"].fillna(houses_clean["total_floors"].median())
    houses_clean["bathroom_count"] = houses_clean["bathroom_count"].fillna(houses_clean["bathroom_count"].median())
    
    
    houses_clean["suspicious_price"] = ((houses_clean["price"] < 500000) | (houses_clean["price"] > 100000000))
    
    
    houses_clean["valid_area"] = (houses_clean["net_sqm"] > 0)
    houses_clean["calculated_price_per_sqm"] = (houses_clean["price"] / houses_clean["net_sqm"])
    houses_clean["price_difference"] = (houses_clean["price_per_sqm"] - houses_clean["calculated_price_per_sqm"]).abs()
    houses_clean["valid_price_per_sqm"] = (houses_clean["valid_area"] &(houses_clean["price_difference"] <= 1))
    return houses_clean


def transform_earthquakes(earthquakes_data):
    earthquakes_clean = earthquakes_data[[
        "EventID",
        "OriginTime",
        "Latitude",
        "Longitude",
        "Depth_km",
        "Magnitude",
        "MagnitudeType",
        "Region"
    ]].copy()
    
    earthquakes_clean["OriginTime"] = pd.to_datetime(earthquakes_clean["OriginTime"],errors="coerce")
    earthquakes_clean["year"] = earthquakes_clean["OriginTime"].dt.year
    earthquakes_clean["month"] = earthquakes_clean["OriginTime"].dt.month
    
    earthquakes_clean["valid_location"] = (earthquakes_clean["Latitude"].between(40.5, 41.6) & earthquakes_clean["Longitude"].between(27.7, 30.3))
    earthquakes_clean["invalid_depth"] = (earthquakes_clean["Depth_km"] <= 0)
    
    earthquakes_clean.loc[earthquakes_clean["invalid_depth"],"Depth_km"] = float("nan")
    
    return earthquakes_clean


def merge_houses_coordinates(houses_clean, district_coordinates):
    coordinates = district_coordinates[[
        "name",
        "latitude",
        "longitude"
    ]].copy()
    
    coordinates = coordinates.rename(
        columns={"name": "district"}
    )
    
    houses_with_coordinates = pd.merge(
        houses_clean,
        coordinates,
        on="district",
        how="left"
    )
    
    return houses_with_coordinates


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
    distance = 2 * 6371 * asin(sqrt(a))

    return distance



def calculate_earthquake_counts(houses_with_coordinates, earthquakes_clean):

    districts = houses_with_coordinates[["district", "latitude", "longitude"]].drop_duplicates()

    results = []

    for _, district in districts.iterrows():

        earthquake_count = 0
        magnitudes = []
        depths = []

        for _, earthquake in earthquakes_clean.iterrows():

            distance = calculate_distance(district["latitude"] , district["longitude"] , earthquake["Latitude"] , earthquake["Longitude"])
            if distance <= 20:

                earthquake_count += 1

                magnitudes.append(earthquake["Magnitude"])

                if pd.notna(earthquake["Depth_km"]):
                    depths.append(earthquake["Depth_km"])


        average_magnitude = (sum(magnitudes) / len(magnitudes)if magnitudes else None)

        max_magnitude = (max(magnitudes)if magnitudes else None)

        average_depth = (sum(depths) / len(depths)if depths else None)

        results.append({"district": district["district"],"earthquake_count_20km": earthquake_count,"average_magnitude_20km": average_magnitude,"max_magnitude_20km": max_magnitude,"average_depth_20km": average_depth})

    return pd.DataFrame(results)


def merge_final_data(houses_with_coordinates, district_earthquakes):
    final_data = pd.merge(houses_with_coordinates , district_earthquakes , on="district" , how="left")
    return final_data