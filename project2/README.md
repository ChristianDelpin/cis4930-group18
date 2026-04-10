# Project 2: Automated Data Pipeline for Countries Data with Currencies, Languages, and Weather

This project fetches data from multiple APIs (REST Countries, Open-Meteo) to collect countries data, currencies, languages, and current weather for capitals, storing results in CSV and SQLite formats. Each run accumulates data and combines related information for analysis.

Link to [API Documentation](https://restcountries.com/) | [Open-Meteo API](https://open-meteo.com/)

## Members

| Name | ID |
|------|----|
| Christian Delpin | cad23j |
| Luis Dominguez | lad24e |
| Leila Kouanda | lk21h |

## Data Pipeline Goals

- Create a database structure that promotes smooth data processing by making tables with only the relevant information
- Provide information on what countries use what currencies and speak what languages
- Fetch current weather data for country capitals using Open-Meteo API
- Combine weather data with country information for enriched analysis
- Fetch all countries data from REST Countries API.
- Extract key fields: name, capital, region, population, area.
- Accumulate results into a single CSV, adding a new batch per run with timestamp.
- Handle failures gracefully and log errors.
- Combine data from multiple API endpoints (currencies and languages) to enrich country information.
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

### Relevancy & Constraints

This API is relevant to real-world transactions by containing a wealth of information. Some included information is the countries' accepted financial currencies that can allow individuals or businesses to understand what kind of payment they should be able to accept from their customers or clients, allowing people to be more informed on how to reach as wide of a clientele as reasonably possible. 

## Database Schema

The project uses SQLite databases for structured storage:

- **Raw Data (`data/raw/countries.db`)**:
  - `all_countries`: Raw JSON dumps from /v3.1/all
  - `currency_countries`: Raw data per currency from /v3.1/currency/{code}
  - `language_countries`: Raw data per language from /v3.1/lang/{code}

- **Processed Data**:
  - `currencies.db`:
    - `currency_list`: (code TEXT PRIMARY KEY, name TEXT, symbol TEXT)
    - `countries_by_currency`: (cca2 TEXT PRIMARY KEY, currencies TEXT) - JSON list of currency codes
  - `languages.db`:
    - `language_list`: (code TEXT PRIMARY KEY, name TEXT, nativeName TEXT)
    - `countries_by_language`: (cca2 TEXT PRIMARY KEY, languages TEXT) - JSON list of language codes
- `weather.db`:
    - `weather_data`: (country TEXT, capital TEXT, latitude REAL, longitude REAL, temperature REAL, windspeed REAL, winddirection REAL, weathercode INTEGER, fetched_at TEXT)
  - `countries.db`: Additional processed country data if needed

## Usage

**Important**: Before running the pipeline for the first time or to reset the data, delete the existing database files to start fresh:
```
rm -f data/raw/countries.db data/processed/currencies.db data/processed/languages.db
```

Install dependencies:
```
pip install -r requirements.txt
```

Run the pipeline:
```
python project2/src/pipeline.py
```

Or use the shell script:
```
./run_pipeline.sh
```

## Data Accumulation

- **CSV Output**: `data/processed/countries.csv` - Accumulates rows across multiple runs
- **SQLite Databases**: 
  - `data/processed/currencies.db` - Currency lists and country-currency mappings
  - `data/processed/languages.db` - Language lists and country-language mappings
  - `data/processed/weather.db` - Current weather data for capitals
  - `data/raw/countries.db` - Raw API responses for auditing
- **Offset Tracking**: `data/processed/offset.txt` - Tracks which batch to fetch next
- **Logs**: `logs/success.log` and `logs/errors.log` - Records all pipeline executions and errors

Each run adds 50 different countries (not duplicates), with each row timestamped in `fetched_at` column. SQLite tables accumulate mappings for currencies and languages.

## Bonus Features

- **Combined APIs**: Integrated weather data from Open-Meteo API with country information for comprehensive analysis.
- **Multiple Data Sources**: Data from REST Countries (countries, currencies, languages) and Open-Meteo (weather) are combined in the pipeline.

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
