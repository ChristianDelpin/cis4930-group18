import sqlite3
from helper_functions import setup_currency_databases
def main():
    setup_currency_databases()
    # conn = sqlite3.connect("project2/data/processed/currencies.db")
    # cursor = conn.cursor()
    # cursor.execute("PRAGMA foreign_key_list(countries_by_currency)")
    # rows = cursor.fetchall()
    # print(rows)
    
    
if __name__ == "__main__":    
    main()