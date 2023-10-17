# create_training_data_from_data_dump

Processes a ROR data dump to generate training data in CSV format.


## Installation:
```bash
pip install -r requirements.txt
```

## Usage:

```bash
python <create_training_data_from_data_dump> -d <input_ROR_data_dump_file> -o <output_CSV_file>
```

## Arguments

- `-d`, `--data_dump`: **Required**. Path to the ROR data dump file.
- `-o`, `--output_file`: Optional. Path to the output CSV file. Default is `ror_data_dump_training_data.csv`.
