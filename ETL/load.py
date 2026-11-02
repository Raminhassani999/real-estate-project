import os

def load_data(houses_clean, earthquakes_clean, district_earthquakes, final_data):

    os.makedirs("output", exist_ok=True)

    
    houses_clean.to_csv("output/clean_housing.csv", index=False)
    earthquakes_clean.to_csv("output/clean_earthquakes.csv", index=False)

    
    district_earthquakes.to_csv("output/district_earthquake_statistics.csv",index=False)

    
    final_data.to_csv("output/final_analysis.csv", index=False)

    print("\nAll four datasets saved successfully!")
