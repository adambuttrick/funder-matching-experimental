# README for Funding Statement Script

## Overview
Generates multiple variations of funding statements from templated text. It processes a CSV file containing funding statements with placeholders and outputs an enhanced version using either a local language model or the OpenAI API.

## Requirements
- Install dependencies using `pip install -r requirements.txt`.
- Local LLM generation assumes [Ollama](https://ollama.ai/) with the [OpenChat model](https://huggingface.co/openchat/openchat_3.5) installed. Ollama is compatible with Mac and Linux. Other local inference methods like [`llama.cpp`](https://github.com/ggerganov/llama.cpp) or [`transformers`](https://huggingface.co/docs/transformers/index) can be used as well, assuming corresponding revisions.
- For OpenAI API usage, set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

## Input Format
The input CSV file should contain a `funding_statement` column. The `funding_statement` is assumed to be a funding statement with placeholders for funders and identifiers, formatted as `{funder_x}` and `{funder_x:funding_identifier}`.

Example:
```
doi,funding_statement
10.1371/journal.pone.0222738,This study was financed in part by the {funder_2} - Finance Code {funder_2:funding_identifier} and {funder_1} - grant number {funder_1:funding_identifier}.
```

## Usage
```
python generate_funding_statement.py -i [input_file.csv] -n [num_generations] -m [model] -o [output_file.csv]
```

Where:
- `[input_file.csv]`: Path to your input CSV file.
- `[num_generations]`: The number of generated statements per input row.
- `[model]`: Either `local` (default) or `openai`.
- `[output_file.csv]`: Path for the output CSV file (default: `generated_statements.csv`).

## Output Format
Output is a CSV file with the original columns from the input file, plus an additional column:
- `generated_statement`: The generated funding statement.


## Notes
- Adjust the `process_data` and the corresponding functions it calls if using a different local inference method.
- The quality of the output depends on the chosen model and input data.