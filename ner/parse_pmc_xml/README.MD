## Overview
Parse PMC XML files and extract the DOI, acknowledgements, and funding information.

## Downloading PMC files
Follow instructions [here](https://www.ncbi.nlm.nih.gov/pmc/tools/pmcaws/) for downloading the Open Acess commercial use subset.

## Installation
```
pip install -r requirements.txt
```

## Usage

- `-d`, `--directory`: Specify the directory containing XML files (required).
- `-o`, `--output_csv`: Set the path for the output CSV file (default: `parsed_xml.csv`).
- `-t`, `--threads`: Number of threads to use for processing (default: 9).

Example:
```
python parse_pmc_xml.py --directory /path/to/xmls --output_csv output.csv --threads 4
```

## Output
- CSV file with columns: `doi`, `acknowledgements`, `funding-information`.

Note: Rows are only added to the CSV for files where DOI and either acknowledgements or funding information are found.