#Time to do the client py as a helper module (hopefully i make it work...)
import requests
import time
from helper_functions import log, log_error 
BASE_URL = "https://restcountries.com/v3.1/all"
#first part of the help module
def get_the_countries():

    try: 
        resp = requests.get(BASE_URL, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        log_error("get_the_countries", "There has been a timeout.")
        return None
    except requests.exceptions.RequestException as a:
        log_error("get_the_countries", "Request could not be made:", a)
        return None
#ok so that was the first function and... not bad
#now for the extract records of the module
#ok so because we changed.... i also have to change all this..... aaaaaaa
def extract_the_records(data):
    if not data:
        return []
    records = []
    for item in data:
        record = {
            "Name": item.get("Name", {}).get("common"),
            "Region": item.get("Region"),
            "Population": item.get("Population"),
            "Area": item.get("Area"),
            "languages": ", ".join(item.get("languages", {}).values()),
            "country_code": item.get("country_code")
#yayyyy i managed to change everything (didnt take that long but still)
        }
        records.append(record)
    return records
#ok and that should be the api_client py 
#yayyyy (we still have a lot to do.....)

        
