import pandas as pd 
import json


def extract_data():
    
    house_prices = pd.read_csv("data/istanbul_apartment_prices_2026.csv")
    earthquakes_data = pd.read_csv("data/koeri_earthquakes_filtered_2026-11-02.csv")
    
    with open("data/turkey_district_coordinates.json", encoding="utf-8") as file:
        locations = json.load(file)
    
    for city in locations:
        if city["name"] == "İstanbul":
            district_coordinates = pd.DataFrame(city["towns"])
            break
    
    return house_prices , earthquakes_data , district_coordinates