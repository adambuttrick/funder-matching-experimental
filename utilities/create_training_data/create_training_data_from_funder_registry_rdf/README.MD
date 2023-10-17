# Funder RDF to CSV Converter

This script is designed to parse Funder RDF data and map them using a JSON file to produce a CSV file suitable for ID lookup view.


## Installation:
```bash
pip install -r requirements.txt
```

## Usage

Download the Funder Registry RDF file from the [Gitlab repo](https://gitlab.com/crossref/open_funder_registry). Download the ROR data dump and generate the ROR-Funder ID mapping with `get_mapped_funders_from_data_dump.py`.

```
python create_training_data_from_funder_registry_rdf.py -f <funder_rdf_file_path> -m <mapping_file_path> [-o <output_file_path>]
```

### Arguments:

- `-f`, `--funder_rdf`: (Required) Path to the Funder RDF file.
  
- `-m`, `--mapping_file`: (Required) Path to the JSON mapping file.

- `-o`, `--output_file`: (Optional) Path to the output CSV file. Default is `funder_registry_training_data.csv`.


## Example

```bash
python script_name.py -f path_to_funder.rdf -m path_to_mapping.json -o output.csv
```