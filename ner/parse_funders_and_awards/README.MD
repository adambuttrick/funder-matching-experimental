## Overview
Extracts and aggregates funding information from Crossref public data files, additionally generating a unique list of DOIs.

## Requirements
```
pip install -r requirements.txt
```

## Usage
```bash
python parse_funders_and_awards.py -d [DIRECTORY] -o [OUTPUT_CSV] -t [THREADS]
```
Options:
- `-d`, `--directory`: Specify the directory containing `.json.gz` files (required).
- `-o`, `--output_csv`: Set the path for the output CSV file (default: `all_funders_and_awards.csv`).
- `-t`, `--threads`: Determine the number of threads for parallel processing (default: 4).

## Outputs
### CSV File
- Format: "DOI", "Funder DOI", "Funder Name", "Awards".

### Unique DOIs File
- A text file (`unique_dois.txt`) listing unique DOIs, each on a separate line.