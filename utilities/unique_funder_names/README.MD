# unique_funder_names

## Description

Extracts unique funder names, computes basic metrics, and outputs the results.

## Usage

```bash
python unique_funder_names.py -i INPUT_FILE [-o OUTPUT_FILE]
```

### Arguments

- `-i`, `--input_file`: **Required**. Path to the input CSV file.
- `-o`, `--output_file`: Optional. Path to the output CSV file. Default is `unique_names.csv`.

## Input CSV Format

CSV containing two columns 'Funder DOIs' and 'Funder Names,' as is generated by count_split_works.py

## Output

1. `unique_names.csv` (or user-defined filename) - A CSV with DOIs, count of occurrences, and unique funder names.

2. `metrics_unique_names.csv` - A CSV with computed metrics, including average, median, mode, and counts in various ranges.
