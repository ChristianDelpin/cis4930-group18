import requests
# import pandas as pd

url = 'https://openlibrary.org/search.json'

endpoint = ''

params = ''

# User-Agent is to identify ourselves, increasing our ratelimit from 1 r/s -> 3 r/s.
# accept is to define the type of response we want to get, meaning `.json()` is not necessary.
headers = {  # TODO: Give proper name
    "User-Agent": "MyAppName/1.0 (cad23j@fsu.edu, lad24e@fsu.edu, lk21h@fsu.edu)",
    "accept": "application/json"
}


# Testing


params = {
    'isbn': '9780140328721'
}

response = requests.get(url, headers=headers, params=params)
print(f"{response.status_code}\n\n{response}")

d=response.json()
print(d)

# End Testing


