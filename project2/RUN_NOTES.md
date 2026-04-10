# Run Notes

## Example Commands

To run the pipeline:
```
python src/pipeline.py
```

Or using the shell script:
```
./run_pipeline.sh
```

## Example Console Output

```
Fetched data for 50 countries (batch from 0 to 50).
Successfully processed and saved 50 countries.
```

## Data Accumulation

Each run appends a new batch of 50 different countries to `data/processed/countries.csv` with timestamps. The offset is tracked in `data/processed/offset.txt` to ensure different data each time.

## Data Accumulation

Each run appends new rows to `data/processed/countries.csv` with a `fetched_at` timestamp, allowing accumulation of data over time.