from api_client import get_the_countries
from api_client import extract_the_records
from storage import save_the_records
# ok had to delete a lot here cause of the change of api so here we gooo
def run_the_pipeline():
    print("[INFO] Getting the country data, wait a second")
    data = get_the_countries()

    records = extract_the_records(data)
    print("f[INFO] extracted the {len(records)} records.")


    save_the_records(records)
    print("[INFO] Pipeline has been completed good job!")

if __name__ == "__main__":
    run_the_pipeline()
# Ending the testing, should be good.... hopefully


