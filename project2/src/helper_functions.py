import datetime
import json
import os
import sqlite3

from datetime import datetime

from project2.src.api_client import extract_the_records, get_the_countries
from project2.src.storage import save_the_records

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

def run_the_pipeline():
    """ Executes the entire data pipeline.
    """
# Luis' code for the pipeline
    log("run_the_pipeline", "Getting the country data, wait a second") # TODO: Change to use logging
    data = get_the_countries()

    records = extract_the_records(data)
    log("run_the_pipeline", "extracted the {len(records)} records.") # TODO: Change to use logging


    save_the_records(records)
    log("run_the_pipeline", "Pipeline has been completed good job!") # TODO: Change to use logging

# Chris' code for the pipeline
    setup_currency_databases()

# Leila's code for the pipeline
