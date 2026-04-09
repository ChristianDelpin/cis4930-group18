#Time to do the client py as a helper module (hopefully i make it work...)
import requests
import time

BASE_URL = "https://openlibrary.org/search.json"
#first part of the help module
def get_from_page(query, page):
    params = {
        "q": query,
        "page": page
    }

    try: 
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout has happened on the page {page}, skipping the page.")
        return None
    except requests.exceptions.RequestException as a:
        print(f"[ERROR] Request could not be made on page {page}: {a}")

#ok so that was the first function and... not bad
#now for the extract records of the module

def extract_the_records(data):
    if not data or "docs" not in data:
        return []
    
    records = []
    for item in data["docs"]:
        record = {
            "Title": item.get("Title"),
            "Author": ", ".join(item.get("author_name", [])),
            "first_published_year": item.get("first_published_year"),
            "isbn": ", ".join(item.get("isbn", [])[:5]),
            "language": ", ".join(item.get("language", [])[:5]),
            "subject": ", ".join(item.get("subject", [])[:5]),
            "edition_count": item.get("edition_count")

        }
        records.append(record)
    return records
#ok and that should be the api_client py 
#yayyyy (we still have a lot to do.....)

        
