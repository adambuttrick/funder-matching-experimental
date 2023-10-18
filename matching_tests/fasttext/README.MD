# fasttext_test

Return funder matches for a given CSV file based on fasttext model predictions.


## Usage

```
python <fasttext_test>.py -i INPUT_CSV -m MAPPING_JSON [-o OUTPUT_CSV] [-p MIN_PROBABILITY]
```

### Arguments

- `-i, --input`: Input CSV file. **Required**
- `-m, --mapping_file`: Mapping JSON file returned from `create_ror_funder_id_mapping_concatenated.py`. **Required**
- `-o, --output`: Output CSV file. Default is `fasttext_results.csv`.
- `-p, --min_fasttext_probability`: Minimum probability level for the fasttext predictor. Default is `0.8`.

### Input CSV Format

Ensure that the input CSV has a column named `funder_name`.

### Output

Generates a CSV with columns:
- Existing columns from the input file.
- `predicted_ror_id`: The predicted ROR ID based on the `funder_name`.
- `prediction_score`: Score for the prediction.
- `predicted_funder_ids`: Mapped funder IDs from the mapping file.
