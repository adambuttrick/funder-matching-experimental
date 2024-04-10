
## Overview
Transforms data from `ner_indexes_funding_statements.py` CSV format into a JSON Lines format for use with [Label Studio](https://github.com/HumanSignal/label-studio). See Label Studio's [pre-annoted import documentation](https://labelstud.io/guide/predictions) for additional details.


## Usage
```
python convert_label_studio_format.py -i <input_file.csv> -o <output_file.jsonl>
```

## Output

A JSONL file formatted for use in Label Studio.