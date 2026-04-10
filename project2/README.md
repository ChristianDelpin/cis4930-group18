# Project 2: Automated Data Pipeline for Countries Data

This project fetches data from the REST Countries API and stores it in CSV format. Each run accumulates more data with timestamps.

Link to [API Documentation](https://restcountries.com/https://restcountries.com/)

## Members

| Name | ID |
|------|----|
| Christian Delpin | cad23j |
| Luis Dominguez | lad24e |
| Leila Kouanda | lk21h |

## Data Pipeline Goals

- Fetch all countries data from REST Countries API.
- Extract key fields: name, capital, region, population, area.
- Accumulate results into a single CSV, adding a new batch per run with timestamp.
- Handle failures gracefully and log errors.
- **Pagination**: Each run fetches a batch of 50 different countries by tracking an offset in `data/processed/offset.txt`.

## How Pagination Works

The pipeline simulates pagination by:
1. Reading the current offset from `data/processed/offset.txt`
2. Fetching a batch of 50 countries starting from that offset
3. Saving the batch to CSV with the next offset value

**Example of offset progression across runs:**
```
Run 1: Offset 0→50   (fetches countries 0-49)
Run 2: Offset 50→100 (fetches countries 50-99)
Run 3: Offset 100→150 (fetches countries 100-149)
Run 4: Offset 150→200 (fetches countries 150-199)
```

Each run appends different countries to `data/processed/countries.csv`, NOT just different timestamps.

## Usage

## Data Pipeline Goals

- Create a database structure that promotes smooth data processing by making tables with only the relevant information
- Provide information on what countries use what currencies

## Relevancy & Constraints

This API is relevant to real-world transactions by containing a wealth of information. Some included information is the countries' accepted financnial currencies that can allow individuals or businesses to understand what kind of payment they should be able to accept from their customers or clients, allowing people to be more informed on how to reach as wide of a clientele as reasonably possible. 

Install dependencies:
```
pip install -r requirements.txt
```

Run the pipeline:
```
python src/pipeline.py
```

Or use the shell script:
```
./run_pipeline.sh
```

## Data Accumulation

- **CSV Output**: `data/processed/countries.csv` - Accumulates rows across multiple runs
- **Offset Tracking**: `data/processed/offset.txt` - Tracks which batch to fetch next
- **Logs**: `logs/pipeline.log` - Records all pipeline executions and errors

Each run adds 50 different countries (not duplicates), with each row timestamped in `fetched_at` column.

## Automation

For cron (Linux/Mac):
```
0 0 * * * /path/to/python /path/to/project/src/pipeline.py
```

For Windows Task Scheduler, create a .bat file:
```
@echo off
C:\path\to\python.exe C:\path\to\project\src\pipeline.py
pause
```
