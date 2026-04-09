#Time to do the client py as a helper module (hopefully i make it work...)
import requests
import time
from helper_functions import log, log_error 
BASE_URL = "https://restcountries.com/v3.1/all"
#first part of the help module
def get_the_countries():
#hmmm i forgot something here, i forgot the status-code check.... oops
    log("get_the_countries", "Starting the process of getting countries API")   
    try: 
        resp = requests.get(BASE_URL, timeout=10)
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
#ok so that was the first function and... not bad
#now for the extract records of the module
#ok so because we changed.... i also have to change all this..... aaaaaaa
def extract_the_records(data):
    log("extract_the_records", "extracting the records!!")
    if not data:
        log_error("extract_the_records", "there is no data..")
        return []
    records = []
    for item in data:
        record = {
            "name": item.get("name", {}).get("common"),
            "region": item.get("region"),
            "population": item.get("population"),
            "area": item.get("area"),
            "languages": ", ".join(item.get("languages", {}).values()),
            "country_code": item.get("country_code")
#yayyyy i managed to change everything (didnt take that long but still)
        }
        records.append(record)
    log("extract_the_records", f"records {len(records)} have been extracted, good job!")
    return records
#ok and that should be the api_client py 
#yayyyy (we still have a lot to do.....)
#ok, with that i think i finished fixing that hehehe
        
