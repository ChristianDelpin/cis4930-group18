# Project 2: Automated Data Pipeline for Countries Data

This project fetches data from the REST Countries API and stores it in CSV format. Each run accumulates more data with timestamps.

Link to [API Documentation](https://restcountries.com/)

## Members

| Name | ID |
|------|----|
| Christian Delpin | cad23j |
| Luis Dominguez | lad24e |
| Leila Kouanda | Lk21h |

## Data Pipeline Goals

- Fetch all countries data from REST Countries API.
- Extract key fields: name, capital, region, population, area.
- Accumulate results into a single CSV, adding a new row per run with timestamp.
- Handle failures gracefully and log errors.

## Usage

Install dependencies:
```
pip install -r requirements.txt
```

Run the pipeline:
```
python src/pipeline.py
```

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
