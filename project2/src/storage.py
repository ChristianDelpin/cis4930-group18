#ok... now that we have api_client.py we need storage one

import os
import pandas as pd
from helper_functions import log, log_error
OUTPUT_PATH = "data/processed/countries_data.csv"

#ok..... first part 
def directories_ensured():
    #makes sure that directories are there and if not then well creates them
    os.makedirs("data/processed", exist_ok=True)

#yay easy enough

def save_the_records(records):
    directories_ensured()

    df= pd.DataFrame(records)

    #ok almost done with this, now we append if the file exist (it should...) and if not it creates it so we make sure everything is ok
    #and im gonna add an error if it does not work then a log_error indicating that
    try:
        if os.path.exists(OUTPUT_PATH):
            df.to_csv(OUTPUT_PATH, mode="a", header=False, index=False)
            log("save_the_records", "Appended {len(records)} rows to the existing csv, congrats.") # TODO: Change to use logging
        else:
            df.to_csv(OUTPUT_PATH, index=False)
            log("save_the_records", "Creating new csv with {len(records)} rows, good job.") # TODO: Change to use logging
    
    except Exception as e:
        log_error("save_the_records", f"Failed to save the records provided, I'm sorry: {e}")
        #ok, this should do it 
