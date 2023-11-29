## Overview
Processes CSV files containing funding statements and DOI, parses these statements using either a local LLM parser or the OpenAI API, and outputs a CSV file with funding references.

## Requirements
- Python 3.x
- Packages from `requirements.txt`
- `ollama` application for local inference
- OpenAI API key set as an environment variable `OPENAI_API_KEY`

## Installation
1. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
2. Install [`ollama`](https://ollama.ai/) and the `mistral-openorca` model for local inference.

## Usage
Run the script with the following command:
```
python parse_acknowledgements.py -i <input_csv_path> -o <output_csv_path> -p <parser_type>
```
- `-i` / `--input_csv`: Path to the input CSV file. (Required)
- `-o` / `--output_csv`: Path to the output CSV file. (Default: `funding_references.csv`)
- `-p` / `--reference_parser`: Parser type, either `local` or `openai`. (Required)

## Input CSV Format
The input CSV must have two columns:
- `doi`: Document Identifier
- `funding_statement`: Funding statement text

## Output CSV Format
The output CSV will have the following columns:
- `doi`: Document Identifier
- `funding_statement`: Original funding statement
- `funder`: Extracted funder information
- `funding_identifier`: Extracted funding identifier

## Error Handling
- The script includes error handling for CSV file reading, JSON decoding, and API response timeouts.
- Retries twice for each record in case of a timeout.