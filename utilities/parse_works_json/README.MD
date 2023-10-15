# parse_json

Convert a series of JSON files retrieved snf saved from the Crossref works endpoint into a single CSV file.

## Usage:

```bash
python <script_name.py> -d <directory_with_json_files> [-o <output_csv_path>]
```

### Arguments:

- `-d` or `--directory`: The directory containing the JSON files you want to process. This argument is **required**.
- `-o` or `--output_csv`: The path where you want to save the generated CSV file. By default, it will save as `works.csv` in the current directory.

## Example:

```bash
python parse_json -d /path/to/json_files -o /path/to/save_file.csv
```

This will process all the JSON files in `/path/to/json_files` and will save the consolidated data in `/path/to/save_file.csv`.