## Overview
Filters a CSV file containing based on a list of DOIs provided in a separate text file. Outputs a new CSV file with only those records that match the DOIs listed.

## Requirements
- Input CSV file (format: must contain a 'doi' column)
- Input text file (format: one DOI per line)

## Usage
```bash
python filter_pmc_w_crossref_funding_assertions.py -c <path_to_csv_file> -t <path_to_txt_file> [-o <path_to_output_file>]
```

- `-c` or `--csv_file`: Path to the CSV file.
- `-t` or `--txt_file`: Path to the text file containing DOIs.
- `-o` or `--output_file` (optional): Path for the output filtered CSV file. Default is `filtered.csv` in the current directory.


## Output
Outputs a CSV file containing only the records that match the DOIs in the provided text file. If no matches are found, it prints "No matching records found." and does not create an output file.