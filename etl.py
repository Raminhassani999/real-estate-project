import pandas as pd 

house_prices = pd.read_csv("data/istanbul_apartment_prices_2026.csv")
earthquakes_data = pd.read_csv("data/koeri_earthquakes_filtered_2026-11-02.csv")

print("House Prices Dataset :" , house_prices.shape)
print("Earthquakes Dataset :" , earthquakes_data.shape)

print("House Prices Columns :")
print(house_prices.columns)

print("Earthquakes Columns:")
print(earthquakes_data.columns)


print("Missing Values In House Prices Dataset")
print(house_prices.isnull().sum())

print("Missing Values In Earthquakes Dataset")
print(earthquakes_data.isnull().sum())

print("Duplicate House Rows" , house_prices.duplicated().sum())
print("Duplicated Earthquake Rows" , earthquakes_data.duplicated().sum())

print("HousePrices Datatypes")
print(house_prices.dtypes)

print("Earthquake Datatypes")
print(earthquakes_data.dtypes)

