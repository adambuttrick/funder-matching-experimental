# find_matched_publisher_asserted_overlap

Calculate the overlap of 'Funder DOIs-Funder Names' pairs between two CSV files.

## Usage

```bash
python script_name.py -m [MATCHED_FILE] -p [PUBLISHER_ASSERTED_FILE] [-o OUTPUT_FILE]
```

## Arguments

- `-m, --matched_file` (Required): Path to the first CSV file.
- `-p, --publisher_asserted_file` (Required): Path to the second CSV file.
- `-o, --output_file` (Optional): Path to the output CSV file. Default is `matched_publisher_asserted_overlap.csv`.

## Output

The script will output:
1. Number of rows from each input CSV file.
2. Number of unique 'Funder DOIs-Funder Names' pairs.
3. The overlap count and percentage between the two CSV files.

## Example

```bash
python find_matched_publisher_asserted_overlap.py -m matched.csv -p publisher_asserted.csv -o overlap.csv
```

## Notes

- Ensure both input CSV files have the columns 'Funder DOIs' and 'Funder Names'.
```