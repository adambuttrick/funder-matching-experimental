## Overview
Transform a CSV file returned from `ner_indexes_funding_statements.py` into a tagged text format suitable for training [Flair](https://github.com/flairNLP/flair) models.


## Usage
```
python convert_flair_training_format.py --input_file [INPUT_CSV] --output_file [OUTPUT_TXT]
```

### Arguments
- `-i` or `--input_file`: Path to the input CSV file.
- `-o` or `--output_file`: Path to the output text file.

## Functionality
1. **Reading CSV**: The script reads a CSV file, expecting a specific format (fields: `doi`, `text`, `type`, `start_index`, `stop_index`).
2. **Tokenization**: It tokenizes the `text` field from the CSV.
3. **Tagging**: Tags tokens as `B-ORG`, `I-ORG` (for organizations), `B-AWARD`, `I-AWARD` (for awards), or `O` (others).
4. **Processing**: Removes leading and trailing punctuation from tokens.
5. **Output**: Generates a text file with tokens and their corresponding tags, line by line.

## Output Format
The output text file contains lines formatted as:

```
[word] [tag]
```

Each line represents a token from the input and its associated tag. The file is ready for use in training NLP models for named entity recognition.