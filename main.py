from ETL.extract import extract_data

from ETL.transform import (
    transform_house_data,
    transform_earthquakes,
    merge_houses_coordinates,
    calculate_earthquake_counts,
    merge_final_data
)

from ETL.load import load_data


# STEP 1: EXTRACT
house_prices, earthquakes_data, district_coordinates = extract_data()

print("EXTRACT COMPLETED")
print("Housing records:", len(house_prices))
print("Earthquake records:", len(earthquakes_data))


# STEP 2: TRANSFORM

# Clean the housing and earthquake datasets
houses_clean = transform_house_data(house_prices)
earthquakes_clean = transform_earthquakes(earthquakes_data)

# Add district coordinates to the housing dataset
houses_with_coordinates = merge_houses_coordinates(
    houses_clean,
    district_coordinates
)

# Calculate earthquake statistics for each district
district_earthquakes = calculate_earthquake_counts(
    houses_with_coordinates,
    earthquakes_clean
)

# Combine housing and earthquake information
final_data = merge_final_data(
    houses_with_coordinates,
    district_earthquakes
)

print("\nTRANSFORM COMPLETED")
print("Cleaned housing records:", len(houses_clean))
print("Cleaned earthquake records:", len(earthquakes_clean))
print("Districts analyzed:", len(district_earthquakes))
print("Final dataset shape:", final_data.shape)


# STEP 3: VALIDATE

# Check that no housing records were lost
assert len(final_data) == len(houses_clean)

# Check that every apartment has earthquake statistics
assert final_data["earthquake_count_20km"].notna().all()

# Check that every apartment has district coordinates
assert final_data[["latitude", "longitude"]].notna().all().all()

print("\nVALIDATION COMPLETED")


# STEP 4: LOAD

load_data(
    houses_clean,
    earthquakes_clean,
    district_earthquakes,
    final_data
)


import pandas as pd

# Read the final CSV to verify the export
check_data = pd.read_csv("output/final_analysis.csv")

print("\nFINAL CSV VALIDATION")
print("Rows and columns:", check_data.shape)

print("Unique apartment IDs:")
print(check_data["listing_id"].nunique())

print("Districts:")
print(check_data["district"].nunique())

print("Missing earthquake counts:")
print(check_data["earthquake_count_20km"].isnull().sum())
