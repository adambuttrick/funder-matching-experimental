# count_split_works

## Description
Processes the works CSV file returned from parse_data_files.py, categorizes data based on the 'DOI Asserted By' values, generates filtered CSVs for each unique 'DOI Asserted By' value, and produces a summary metrics CSV containing counts and percentages of each 'DOI Asserted By' value.


## Usage
Run the script using the command below:

```
python count_split_works.py -i /path/to/your/input.csv
```

## Parameters
- `-i` or `--input_csv`: The path to the input CSV file. This parameter is required.

## Output
For each unique 'DOI Asserted By' value in the input CSV:
- A filtered CSV file is generated with rows containing that specific value.
- If the value is empty, the file will be named `_funder_asserted_by_null.csv`.

Additionally, a summary metrics CSV named `{input_file_name}_funder_assertion_metrics.csv` is generated. This file contains three columns: 'DOI Asserted By', 'Count', and 'Percentage', detailing the distribution of 'DOI Asserted By' values in the input CSV.