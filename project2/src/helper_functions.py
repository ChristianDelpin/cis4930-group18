import datetime
import json
import os
import sqlite3
import requests
import pandas as pd

from datetime import datetime

#from storage import save_the_records

BASE_URL = "https://restcountries.com/v3.1/"
OUTPUT_PATH = "project2/data/processed/countries_data.csv"

def save_as_sqlite(DataFrame, path, table_name, if_exists="append", index=False) -> bool:
    """Save a pandas DataFrame to SQLite, creating the table if necessary.

    Checks if the table exists; if not, creates it using the DataFrame schema.
    Then appends or replaces the data based on if_exists parameter.

    Args:
        DataFrame: pandas DataFrame to save.
        path: path to the SQLite database file.
        table_name: table name to save to.
        if_exists: behavior if table exists (default: "append").
        index: whether to write DataFrame index as a column.

    Returns:
        bool: whether saving was successful.
    """
    try:
        for col in DataFrame.columns:
            if DataFrame[col].apply(lambda x: isinstance(x, (list, dict))).any():
                DataFrame[col] = DataFrame[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)

        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                (table_name,)
            )
            table_exists = cursor.fetchone() is not None

            # If table doesn't exist, create it
            if not table_exists:
                DataFrame.to_sql(table_name, conn, if_exists="replace", index=index)
                log("save_as_sqlite", f"Table '{table_name}' created and DataFrame saved successfully.")
            else:
                DataFrame.to_sql(table_name, conn, if_exists=if_exists, index=index)
                log("save_as_sqlite", f"DataFrame saved into SQLite database successfully.")

            return True
    except Exception as e:
        log_error("save_as_sqlite", f"Failed to save DataFrame: {e}")
        return False

def setup_currency_databases():
    """Helper function to create and populate the currency databases.
    
    Calls the necessary functions to fetch currency data and build the
    countries-by-currency table in the processed currencies database.
    """
    from currency import get_all_currency_codes, add_currency_to_countries
    get_all_currency_codes()
    add_currency_to_countries()

def log(function_name, message):
    """Logs successful operations.
    
    Parameters:
        function_name: The name of the function where the success occurred.
        message: The success message.
    """
    log_file_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'success.log')
    
    mode = 'a' if os.path.exists(log_file_path) else 'w'
    
    with open(log_file_path, mode) as f:
        f.write(f"{datetime.now()}  {function_name}: {message}\n")

def log_error(function_name, error_message):
    """Logs errors.
    
    Parameters:
        function_name: The name of the function where the error occurred.
        error_message: The error message.
    """
    log_file_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'errors.log')
    
    mode = 'a' if os.path.exists(log_file_path) else 'w'
    
    with open(log_file_path, mode) as f:
        f.write(f"{datetime.now()}  {function_name}: {error_message}\n")

def get_the_countries():
#hmmm i forgot something here, i forgot the status-code check.... oops
    log("get_the_countries", "Starting the process of getting countries API")   
    try: 
        resp = requests.get(f"{BASE_URL}all", timeout=10)
        if resp.status_code == 200:
            log("get_the_countries", "Status code 200 is doing great")
        else:
            log_error("get_the_countries", f"there was an error with the status code: {resp.status_code}")

        resp.raise_for_status()
        data = resp.json()
        
        log("get_the_countries", f"Succesfully gotten the {len(data)} records")
        return data
    
    except requests.exceptions.Timeout:
        log_error("get_the_countries", "There has been a timeout.")
        return None
    except requests.exceptions.RequestException as e:
        log_error("get_the_countries", f"Request could not be made: {e}")
        return None

def extract_the_records(data):
    log("extract_the_records", "extracting the records!!")
    if not data:
        log_error("extract_the_records", "there is no data..")
        return []
    records = []
    for item in data:
        record = {
            "name": item.get("name", {}).get("common"),
            "official_name": item.get("name", {}).get("official"),
            "region": item.get("region"),
            "subregion": item.get("subregion"),
            "population": item.get("population"),
            "capital": ", ".join(item.get("capital", [])),
            "languages": ", ".join(item.get("languages", {}).values()),
            "area": item.get("area"),
            "country_code": item.get("cca2"),
            "flag_url": item.get("flags", {}).get("png")
#yayyyy i managed to change everything (didnt take that long but still)
        }
        records.append(record)
    log("extract_the_records", f"records {len(records)} have been extracted, good job!")
    return records

def directories_ensured():
    #makes sure that directories are there and if not then well creates them
    os.makedirs("project2/data/processed", exist_ok=True)


def save_the_records(records):
    directories_ensured()

    df= pd.DataFrame(records)

    #ok almost done with this, now we append if the file exist (it should...) and if not it creates it so we make sure everything is ok
    #and im gonna add an error if it does not work then a log_error indicating that
    try:
        if os.path.exists(OUTPUT_PATH):
            df.to_csv(OUTPUT_PATH, mode="a", header=False, index=False)
            log("save_the_records", f"Appended {len(records)} rows to the existing csv, congrats.") # TODO: Change to use logging
        else:
            df.to_csv(OUTPUT_PATH, index=False)
            log("save_the_records", f"Creating new csv with {len(records)} rows, good job.") # TODO: Change to use logging
    
    except Exception as e:
        log_error("save_the_records", f"Failed to save the records provided, I'm sorry: {e}")
        #ok, this should do it 




def run_pipeline():
    """ Executes the entire data pipeline.
    """
# Luis' code for the pipeline
    log("run_the_pipeline", "Getting the country data, wait a second")
    data = get_the_countries()

    records = extract_the_records(data)
    log("run_the_pipeline", f"extracted the {len(records)} records.") 


    save_the_records(records)
    log("run_the_pipeline", "Pipeline has been completed good job!") 

# Chris' code for the pipeline
    setup_currency_databases()

# Leila's code for the pipeline
