## Overview
Extracts and aggregates funding information from Crossref public data file.

## Requirements
```
pip install -r requirements.txt
```

## Usage
```bash
python parse_funders_and_awards.py -d [DIRECTORY] -o [OUTPUT_CSV] -t [THREADS]
```
- `-d`, `--directory`: Directory containing `.json.gz` files (required).
- `-o`, `--output_csv`: Path for the output CSV file (default: `all_funders_and_awards.csv`).
- `-t`, `--threads`: Number of threads to use for parallel processing (default: 4).

## CSV Output
- Format: "DOI", "Funder DOI", "Funder Name", "Awards".
