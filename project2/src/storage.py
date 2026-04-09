#ok... now that we have api_client.py we need storage one

import os
import pandas as pd

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

    if os.path.exists(OUTPUT_PATH):
        df.to_csv(OUTPUT_PATH, mode="a", header=False, index=False)
        print(f"[INFO] Appended {len(records)} rows to the existing csv, congrats.")

    else:
        df.to_csv(OUTPUT_PATH, index=False)
        print(f"[INFO] Creating new csv with {len(records)} rows, good job.")
