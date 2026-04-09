import pandas as pd
import requests
import sqlite3
import json
from collections import defaultdict

from helper_functions import save_as_sqlite

# Raw DB
db_country_raw = "project2/data/raw/countries.db"

# Processed DB
db_currency_processed = "project2/data/processed/currencies.db"
db_country_processed = "project2/data/processed/countries.db"

# Tables
table_country_currencies = "countries_by_currency"
table_currency_list = "currency_list"



def process_currency(currency) -> bool:
    """Process individual currency data by fetching, transforming, and saving to a SQLite database.
    
    Retrieves country data for a given currency code, saves the raw data,
    then creates and saves a processed summary.
    
    Parameters:
        `currency`: Currency code to process. Example: "USD", "EUR"
    
    Returns:
        `bool`: Whether processing was successful.
    """
    response = get_countries_by_currency(currency)
    if not response:
        print("Failed to retrieve data from API.")
        return False
    
    try:
        raw_df = pd.DataFrame(response)
        
        # Save raw data (creates table if needed)
        save_as_sqlite(raw_df, db_country_raw, table_country_currencies)
        
        # Process and save summary (creates table if needed)
        processed_df = pd.DataFrame({
            "country_code": raw_df["cca2"],
            "common_name": raw_df["name"].apply(lambda x: x["common"]),
            "currencies": raw_df["currencies"].apply(lambda x: list(x.keys())[0] if isinstance(x, dict) else None)
        })
        save_as_sqlite(processed_df, db_country_processed, table_country_currencies)
        
        return True
    except Exception as e:
        print(f"Error occurred while processing currency {currency}: {e}")
        return False

def get_all_currency_codes():
    try:
        url = "https://restcountries.com/v3.1/all"
        params = {"fields": "currencies"}
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        # Save raw data
        raw_df = pd.DataFrame(data)
        save_as_sqlite(raw_df, db_country_raw, "all_countries")

        # Taking the response and extracting the important bits into a df

        rows = []
        for country in data:
            for code, info in country["currencies"].items():
                rows.append({
                    "code": code,
                    "name": info["name"],
                    "symbol": info["symbol"]
                })

        df = pd.DataFrame(rows)
        df = df.drop_duplicates(subset=["code"], keep="first").reset_index(drop=True)

        with sqlite3.connect(db_currency_processed) as conn:
            conn.execute(f"DROP TABLE IF EXISTS {table_currency_list}")
            conn.execute(
                f"CREATE TABLE {table_currency_list} (code TEXT PRIMARY KEY, name TEXT, symbol TEXT)"
            )
            df.to_sql(table_currency_list, conn, if_exists="append", index=False)

    except requests.exceptions.RequestException as e:
        print(f"[get_all_currency_codes()] Request failed: {e}")

def add_currency_to_countries():
    conn = sqlite3.connect(db_currency_processed)
    cursor = conn.cursor()

    # Get all currency codes
    cursor.execute(f"SELECT code FROM {table_currency_list}")
    codes = [row[0] for row in cursor.fetchall()]

    country_to_currencies = defaultdict(list)

    for code in codes:
        try:
            response = requests.get(f"https://restcountries.com/v3.1/currency/{code}")
            response.raise_for_status()
            data = response.json()
            # Save raw data
            raw_df = pd.DataFrame(data)
            raw_df['currency_code'] = code
            save_as_sqlite(raw_df, db_country_raw, "currency_countries")
            
            for country in data:
                cca2 = country['cca2']
                country_to_currencies[cca2].append(code)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data for currency {code}: {e}")

    # Create the table
    cursor.execute(f"DROP TABLE IF EXISTS {table_country_currencies}")

    # TODO: Add foreign key reference to cca2 when countries table is created
    cursor.execute(f"CREATE TABLE {table_country_currencies} (cca2 TEXT PRIMARY KEY, currencies TEXT)")

    # Insert data
    for cca2, currencies in country_to_currencies.items():
        cursor.execute(f"INSERT INTO {table_country_currencies} (cca2, currencies) VALUES (?, ?)", (cca2, json.dumps(currencies)))

    conn.commit()
    conn.close()

def get_countries_by_currency(currency_code):
    try:
        url = f"https://restcountries.com/v3.1/currency/{currency_code}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[get_countries_by_currency()] Request failed: {e}")
        return None
