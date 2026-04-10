import pandas as pd
import requests
import sqlite3
import json
from collections import defaultdict

from helper_functions import log, log_error, save_as_sqlite

# Raw DB
db_country_raw = "../data/raw/countries.db"

# Processed DB
db_weather_processed = "../data/processed/weather.db"
db_country_processed = "../data/processed/countries.db"

# Tables
table_weather_data = "weather_data"

def get_weather_for_capitals():
    """Fetches current weather data for country capitals using Open-Meteo API."""

    try:
        # First, get countries with capitals and coordinates
        url = "https://restcountries.com/v3.1/all"
        params = {"fields": "name,capital,latlng"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if not response.status_code == 200:
            log_error("get_weather_for_capitals", f"API request failed with status code: {response.status_code}")
            return
        
        data = response.json()
        
        weather_records = []
        for country in data:
            capital = country.get("capital", [None])[0]
            latlng = country.get("latlng", [])
            if capital and len(latlng) >= 2:
                lat, lon = latlng[0], latlng[1]
                try:
                    weather_url = "https://api.open-meteo.com/v1/forecast"
                    weather_params = {
                        "latitude": lat,
                        "longitude": lon,
                        "current_weather": "true"
                    }
                    weather_response = requests.get(weather_url, params=weather_params, timeout=10)
                    weather_response.raise_for_status()
                    
                    weather_data = weather_response.json()
                    current_weather = weather_data.get("current_weather", {})
                    
                    record = {
                        "country": country["name"]["common"],
                        "capital": capital,
                        "latitude": lat,
                        "longitude": lon,
                        "temperature": current_weather.get("temperature"),
                        "windspeed": current_weather.get("windspeed"),
                        "winddirection": current_weather.get("winddirection"),
                        "weathercode": current_weather.get("weathercode"),
                        "fetched_at": pd.Timestamp.now().isoformat()
                    }
                    weather_records.append(record)
                    
                except requests.exceptions.RequestException as e:
                    log_error("get_weather_for_capitals", f"Failed to fetch weather for {capital}: {e}")
                    continue
        
        df = pd.DataFrame(weather_records)
        
        with sqlite3.connect(db_weather_processed) as conn:
            conn.execute(f"DROP TABLE IF EXISTS {table_weather_data}")
            df.to_sql(table_weather_data, conn, if_exists="append", index=False)
        
        log("get_weather_for_capitals", f"Successfully saved weather data for {len(weather_records)} capitals")
        
    except requests.exceptions.RequestException as e:
        log_error("get_weather_for_capitals", f"Request failed: {e}")

def get_weather_by_country(country_name):
    """Fetches current weather for a specific country's capital.
    
    Parameters:
        country_name: Name of the country
    
    Returns:
        dict or None: Weather data if successful, otherwise None.
    """
    
    try:
        # Get country data
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return None
            
        country = data[0]
        capital = country.get("capital", [None])[0]
        latlng = country.get("latlng", [])
        
        if not capital or len(latlng) < 2:
            return None
            
        lat, lon = latlng[0], latlng[1]
        
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        weather_response.raise_for_status()
        
        return weather_response.json()
        
    except requests.exceptions.RequestException as e:
        log_error("get_weather_by_country", f"Request failed for {country_name}: {e}")
        return None