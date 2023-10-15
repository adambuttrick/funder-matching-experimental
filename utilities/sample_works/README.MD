# sample_works

Sample a specific number of rows from a given works CSV file.

## Usage

```bash
python csv_sampler.py -i INPUT_FILE -s SAMPLE_SIZE [-o OUTPUT_FILE]
```

#### Arguments:

- `-i` or `--input_file` (required): Path to the input CSV file.
  
- `-s` or `--sample_size` (required): The number of rows you'd like to sample from the CSV.
  
- `-o` or `--output_file` (optional): Path to save the output CSV file. If not provided, it will be saved as `sampled.csv` by default.

### Example:

```bash
python sample_works.py -i data.csv -s 100 -o sampled_data.csv
```

This will sample 100 rows from `data.csv` and save it to `sampled_data.csv`.