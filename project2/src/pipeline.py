from helper_functions import run_pipeline

def main():
    run_pipeline()
    
if __name__ == "__main__":    
    main()import requests
from datetime import datetime
import pandas as pd
from storage import save_to_csv
import os

# API details
API_URL = "https://restcountries.com/v3.1/all"
params = {"fields": "name,capital,region,population,area"}

def fetch_countries_data():
    # Since the API doesn't have real pagination, we simulate it by fetching all and slicing
    # Read the current offset from file
    offset_file = "data/processed/offset.txt"
    if os.path.exists(offset_file):
        with open(offset_file, 'r') as f:
            offset = int(f.read().strip())
    else:
        offset = 0
    
    # Set batch size, like 50 countries per run
    batch_size = 50
    
    try:
        response = requests.get(API_URL, params=params, timeout=10, headers={'User-Agent': 'Python/3.12'})
        response.raise_for_status()
        data = response.json()
        
        # Simulate pagination: take a slice from offset to offset + batch_size
        # This way, each run gets different countries
        end_index = min(offset + batch_size, len(data))
        batch_data = data[offset:end_index]
        
        # Update offset for next run
        new_offset = end_index
        os.makedirs(os.path.dirname(offset_file), exist_ok=True)
        with open(offset_file, 'w') as f:
            f.write(str(new_offset))
        
        # Extract relevant fields
        countries = []
        for country in batch_data:
            record = {
                "name": country.get("name", {}).get("common", "Unknown"),
                "capital": country.get("capital", [None])[0] if country.get("capital") else None,
                "region": country.get("region", "Unknown"),
                "population": country.get("population", 0),
                "area": country.get("area", 0.0),
                "fetched_at": datetime.now().isoformat()
            }
            countries.append(record)
        print(f"Fetched data for {len(countries)} countries (batch from {offset} to {end_index}).")
        return countries
    
    except requests.exceptions.Timeout:
        print("Request timed out, will skip this run.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
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