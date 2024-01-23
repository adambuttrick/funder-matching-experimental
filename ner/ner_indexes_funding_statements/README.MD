
## Overview
Verifies and indexes the occurrences of funders and associated awards within the text of funding statements, adhering to a minimum count of funders for inclusion.

## Usage
- `-f/--funder_csv`: Path to the funder CSV file.
- `-p/--publication_csv`: Path to the publication CSV file.
- `-o/--output`: Output path for the generated CSV file (default: `filtered_ner_indexes_funding_statements.csv`).

Example:
```
python ner_indexes_funding_statements.py -f path/to/funder.csv -p path/to/publication.csv -o path/to/output.csv
```

## Output
A CSV file containing indexed funding information, including DOI, text, start and stop indexes of funders and awards, and type (funder or award).

## Notes
- Filters out funding statements with non-printable characters.
- Minimum default funder count is set to 3 for inclusion in the output.
- Input files are derived from `parse_funders_and_awards.py` and `filter_pmc_w_crossref_funding_assertions.py`