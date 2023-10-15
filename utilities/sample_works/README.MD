Certainly, here's your updated README to reflect the new feature:

---

# sample_works

Sample a specific number of rows from a given works CSV file. Additionally, filter the rows based on a mapping file before sampling.

## Usage

```bash
python sample_works.py -i INPUT_FILE -s SAMPLE_SIZE [-o OUTPUT_FILE] [-m MAPPING_FILE]
```

#### Arguments:

- `-i` or `--input_file` (required): Path to the input CSV file.
  
- `-s` or `--sample_size` (required): The number of rows you'd like to sample from the CSV.
  
- `-o` or `--output_file` (optional): Path to save the output CSV file. If not provided, it will be saved with a default name based on the input file name.

- `-m` or `--mapping_file` (optional): Path to a newline delimited text file. The CSV rows will be filtered based on whether any value from this mapping is found in the "Funder DOIs" field before sampling.

### Example:

```bash
python sample_works.py -i data.csv -s 100 -o sampled_data.csv -m mapping.txt
```

This will filter the rows of `data.csv` based on the values in `mapping.txt`, then sample 100 rows from the filtered data and save it to `sampled_data.csv`.