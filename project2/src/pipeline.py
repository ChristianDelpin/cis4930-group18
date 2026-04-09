import requests
from datetime import datetime
import pandas as pd
from storage import save_to_csv

# API details
BASE_URL = "https://restcountries.com/v3.1/all"
params = {"fields": "name,capital,region,population,area"}

def fetch_countries_data():
    try:
        # HTTP & requests basics:
        # - requests.get() sends a GET request to the URL
        # - params= passes query parameters, automatically URL-encoded
        # - timeout= prevents hanging on slow responses
        # - response.status_code: 200 for success, 400 for bad request, etc.
        # - response.raise_for_status() raises exception for non-2xx codes
        # - response.json() parses JSON response body into Python dict/list
        response = requests.get(BASE_URL, params=params, timeout=10, headers={'User-Agent': 'Python/3.12'})
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant fields
        countries = []
        for country in data:
            record = {
                "name": country.get("name", {}).get("common", "Unknown"),
                "capital": country.get("capital", [None])[0] if country.get("capital") else None,
                "region": country.get("region", "Unknown"),
                "population": country.get("population", 0),
                "area": country.get("area", 0.0),
                "fetched_at": datetime.now().isoformat()
            }
            countries.append(record)
        
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