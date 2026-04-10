import pandas as pd
import requests
import sqlite3
import json
from collections import defaultdict

from helper_functions import log, log_error, save_as_sqlite

# Raw DB
db_country_raw = "../data/raw/countries.db"

# Processed DB
db_language_processed = "../data/processed/languages.db"
db_country_processed = "../data/processed/countries.db"

# Tables
table_country_languages = "countries_by_language"
table_language_list = "language_list"

def get_all_language_codes():
    """Fetches all language codes from the REST Countries API and saves them to a SQLite database."""

    try:
        url = "https://restcountries.com/v3.1/all"
        params = {"fields": "languages"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if not response.status_code == 200:
            log_error("get_all_language_codes", f"API request failed with status code: {response.status_code}")
            return
        
        data = response.json()
        # Save raw data
        raw_df = pd.DataFrame(data)
        save_as_sqlite(raw_df, db_country_raw, "all_countries_languages")

        # Extract language codes
        rows = []
        for country in data:
            if "languages" in country:
                for code, info in country["languages"].items():
                    if isinstance(info, dict):
                        name = info.get("name", "Unknown")
                        nativeName = info.get("nativeName", "Unknown")
                    else:
                        name = str(info)
                        nativeName = str(info)
                    rows.append({
                        "code": code,
                        "name": name,
                        "nativeName": nativeName
                    })
        
        df = pd.DataFrame(rows)
        df = df.drop_duplicates(subset=["code"], keep="first").reset_index(drop=True)

        with sqlite3.connect(db_language_processed) as conn:
            conn.execute(f"DROP TABLE IF EXISTS {table_language_list}")
            conn.execute(
                f"CREATE TABLE {table_language_list} (code TEXT PRIMARY KEY, name TEXT, nativeName TEXT)"
            )
            df.to_sql(table_language_list, conn, if_exists="append", index=False)

    except requests.exceptions.RequestException as e:
        log_error("get_all_language_codes", f"Request failed: {e}")

def add_language_to_countries():
    """ Adds language information to the countries table."""

    conn = sqlite3.connect(db_language_processed)
    cursor = conn.cursor()

    # Get all language codes
    cursor.execute(f"SELECT code FROM {table_language_list}")
    codes = [row[0] for row in cursor.fetchall()]

    country_to_languages = defaultdict(list)

    for code in codes:
        try:
            response = requests.get(f"https://restcountries.com/v3.1/lang/{code}")
            response.raise_for_status()

            if not response.status_code == 200:
                log_error("add_language_to_countries", f"API request for language {code} failed with status code: {response.status_code}")
                continue

            data = response.json()
            # Save raw data
            raw_df = pd.DataFrame(data)
            raw_df['language_code'] = code
            save_as_sqlite(raw_df, db_country_raw, "language_countries")
            
            for country in data:
                cca2 = country['cca2']
                country_to_languages[cca2].append(code)
        except requests.exceptions.Timeout as e:
            log_error("add_language_to_countries", f"API request timed out for language {code}")
        
        except requests.exceptions.RequestException as e:
            log_error("add_language_to_countries", f"API request failed for language {code}: {e}")

    # Create the table
    cursor.execute(f"DROP TABLE IF EXISTS {table_country_languages}")

    cursor.execute(f"CREATE TABLE {table_country_languages} (cca2 TEXT PRIMARY KEY, languages TEXT)")

    # Insert data
    for cca2, languages in country_to_languages.items():
        cursor.execute(f"INSERT INTO {table_country_languages} (cca2, languages) VALUES (?, ?)", (cca2, json.dumps(languages)))

    conn.commit()
    conn.close()

def get_countries_by_language(language_code):
    """Fetches country data for a given language code from the REST Countries API.
    
    Parameters:
        language_code: Language code to query. Example: "en", "fr"
    
    Returns:
        dict or None: API response as a dictionary if successful, otherwise None.
    """

    try:
        url = f"https://restcountries.com/v3.1/lang/{language_code}"
        response = requests.get(url)
        response.raise_for_status()

        if not response.status_code == 200:
            log_error("get_countries_by_language", f"API request failed with status code: {response.status_code}")
            return None

        return response.json()
    except requests.exceptions.RequestException as e:
        log_error("get_countries_by_language", f"Request failed: {e}")
        return None