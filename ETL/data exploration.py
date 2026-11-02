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

print("Duplicated Housing ID's")
print(house_prices['listing_id'].duplicated().sum())

print("Duplicated Earthquakes ID's")
print(earthquakes_data['EventID'].duplicated().sum())

print("Minimum Housing Prices" , house_prices['price'].min())
print("Maximum Housing Prices" , house_prices['price'].max())

print("Minimum Magnitude" , earthquakes_data['Magnitude'].min())
print("Maximum Magnitude" , earthquakes_data['Magnitude'].max())

print("10 most expensive apartments:")
print(house_prices.nlargest(10 , "price")[["price", "district", "gross_sqm", "rooms", "building_age"]])

print("10 cheapest apartments:")
print(house_prices.nsmallest(10 , 'price')[["price", "district", "gross_sqm", "rooms", "building_age"]])


print("Housing price statistics:")
print(house_prices['price'].describe())

print("Listings above 100 million TRY:")
print((house_prices['price'] > 100000000).sum())

print("Listings below 500,000 TRY:")
print((house_prices['price'] < 500000).sum())