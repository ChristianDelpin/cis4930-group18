import requests
from datetime import datetime
import pandas as pd
from storage import save_to_csv

# API details
API_URL = "https://restcountries.com/v3.1/all"
params = {"fields": "name,capital,region,population,area"}

def fetch_countries_data():
    # For pagination:
    # page = 1
    # all_items = []
    # while True:
    #     params["page"] = page
    #     response = requests.get(API_URL, params=params, timeout=10)
    #     response.raise_for_status()
    #     data = response.json()
    #     items = data.get("items", [])
    #     if not items:
    #         break
    #     all_items.extend(items)
    #     page += 1
    #     if page > 10:  # limit to avoid huge downloads
    #         break
    # return all_items
    
    try:
        response = requests.get(API_URL, params=params, timeout=10, headers={'User-Agent': 'Python/3.12'})
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant fields that existe in params at line 6 to 8
        countries = []
        for country in data:
            record = {
                "name": country.get("name", {}).get("common", "Unknown"),
                "capital": country.get("capital", [None])[0] if country.get("capital") else None,
                "region": country.get("region", "Unknown"),
                "population": country.get("population", 0),
                "area": country.get("area", 0.0)
            }
            countries.append(record)
        print(f"Fetched data for {(countries)} countries.")
        return countries
    
    except requests.exceptions.Timeout:
        print("Request timed out, will skip this run.")
        return []

def main():
    countries_data = fetch_countries_data()
    
    if countries_data:
        df = pd.DataFrame(countries_data)
        
        # Save to CSV
        csv_path = "data/processed/countries.csv"
        save_to_csv(df, csv_path)
        
        print(f"Successfully processed and saved {len(df)} countries.")
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()