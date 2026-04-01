import requests
import pandas as pd
import sqlite3
import json


url = 'https://openlibrary.org/'
endpoint = ''
params = ''
timeout = 10
# User-Agent is to identify ourselves, increasing our ratelimit from 1 r/s -> 3 r/s.
# accept is to define the type of response we want to get, meaning `.json()` is not necessary.
headers = {  # TODO: Give proper name
    "User-Agent": "MyAppName/1.0 (cad23j@fsu.edu, lad24e@fsu.edu, lk21h@fsu.edu)",
    "accept": "application/json"
}


# Testing

endpoint = 'isbn/'
params = '9780544003415'
fully_qualified_url = url+endpoint+params

response = requests.get(fully_qualified_url, headers=headers,timeout=timeout)
print(f"{response.status_code}\n\n{response}")

data=response.json()
print(data)

df = pd.DataFrame([data])

# Convert DataFrame object into a .SQLite file
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)


with sqlite3.connect("../data/raw/test.sqlite") as conn:
    df.to_sql("testing_table", conn, if_exists="append",index=False)    


# End Testing


