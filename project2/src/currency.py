import pandas as pd
import requests
import sqlite3
import json
from collections import defaultdict

from helper_functions import log, log_error, save_as_sqlite

# Raw DB
db_country_raw = "../data/raw/countries.db"

# Processed DB
db_currency_processed = "../data/processed/currencies.db"
db_country_processed = "../data/processed/countries.db"

# Tables
table_country_currencies = "countries_by_currency"
table_currency_list = "currency_list"

def get_all_currency_codes():
    """Fetches all currency codes from the REST Countries API and saves them to a SQLite database."""

    try:
        url = "https://restcountries.com/v3.1/all"
        params = {"fields": "currencies"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if not response.status_code == 200:
            log_error("get_all_currency_codes", f"API request failed with status code: {response.status_code}")
            return
        
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
        log_error("get_all_currency_codes", f"Request failed: {e}")

def add_currency_to_countries():
    """ Adds currency information to the countries table."""

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

            if not response.status_code == 200:
                log_error("add_currency_to_countries", f"API request for currency {code} failed with status code: {response.status_code}")
                continue

            data = response.json()
            # Save raw data
            raw_df = pd.DataFrame(data)
            raw_df['currency_code'] = code
            save_as_sqlite(raw_df, db_country_raw, "currency_countries")
            
            for country in data:
                cca2 = country['cca2']
                country_to_currencies[cca2].append(code)
        except requests.exceptions.Timeout as e:
            log_error("add_currency_to_countries", f"API request timed out for currency {code}")
        
        except requests.exceptions.RequestException as e:
            log_error("add_currency_to_countries", f"API request failed for currency {code}: {e}")

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
    """    Fetches country data for a given currency code from the REST Countries API.
        Parameters:
            `currency_code`: Currency code to query. Example: "USD", "EUR"
        
        Returns:
            `dict` or `None`: API response as a dictionary if successful, otherwise None.
    """

    try:
        url = f"https://restcountries.com/v3.1/currency/{currency_code}"
        response = requests.get(url)
        response.raise_for_status()

        if not response.status_code == 200:
            log_error("get_countries_by_currency", f"Unexpected status code: {response.status_code}")
            return None

        return response.json()
    except requests.exceptions.RequestException as e:
        log_error("get_countries_by_currency", f"Request failed: {e}")
        return None
