# create_ror_funder_id_mapping

Generates a mapping between ROR IDs and Funder IDs from the ROR data dump file.


## Usage

```bash
python <create_ror_funder_id_mapping.py>.py -d <path_to_ror_data_dump> [-o <output_file_path>]
```

### Arguments
- `-d` or `--data_dump`: **Required**. Path to the ROR data dump file.
- `-o` or `--output_file`: Optional. Path to save the output JSON file. Default is `ror-funder_mapping.json`.


## Example

```bash
python <create_ror_funder_id_mapping.py>.py -d ror_data.json -o mapped_ids.json
```

This will read `ror_data.json`, generate the mapping, and save it to `mapped_ids.json`.
```
