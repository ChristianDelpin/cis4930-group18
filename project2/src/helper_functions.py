import json
import sqlite3

def save_as_sqlite(DataFrame):
    try:
        for col in DataFrame.columns:
            if DataFrame[col].apply(lambda x: isinstance(x, (list, dict))).any():
                DataFrame[col] = DataFrame[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)

        with sqlite3.connect("data/raw/test.sqlite") as conn:
            DataFrame.to_sql("testing_table", conn, if_exists="append",index=False)
            print("DataFrame saved into SQLite database successfully")
            return True
    except Exception as e:
        print(f"[save_as_sqlite()] Saving failed: {e}")
        return False
