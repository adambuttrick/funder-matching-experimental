# parse_data_files

## Description

Parse data from the Crossref public data files (compressed as .json.gz) into a single deduplicated CSV file. The script specifically extracts data related to DOI, creation date, publication date, and funder details from each file.


## Usage

```bash
python <script_name>.py -d /path/to/json_files/ -o /path_to_output/output.csv
```

### Arguments

- `-d, --directory` (Required): Directory containing `.json.gz` files that you wish to convert.
- `-o, --output_csv` (Optional): Path to save the generated CSV file. Default is `works.csv`.