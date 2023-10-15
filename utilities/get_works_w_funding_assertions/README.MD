# get_works_w_funding_assertions

## `get_works_w_funding_assertions.py` 

Fetches works with funding assertions from the Crossref API based on a specified date range.

### Installation:
```
pip install -r requirements.txt
```

### Usage:
```
python get_works_w_funding_assertions.py -s START_DATE -e END_DATE [optional args]
```

### Arguments:

- `-s`, `--start_date`: Start date for filtering works. (Required)
  
  Format: `YYYY-MM-DD`

- `-e`, `--end_date`: End date for filtering works. (Required)
  
  Format: `YYYY-MM-DD`

- `-u`, `--user_agent`: User Agent for the request. Format: `mailto:name@email` (Optional)

- `-t`, `--token`: Crossref Metadata Plus API token. (Optional)


### Outputs:

Data is saved in a series of JSON files, each corresponding to a page of results from the Crossref API. They are saved in a directory named in the format: `{start_date}_{stop_date}_works_w_funding_assertions`.

Each file is named in the format: `{start_date}-{stop_date}_page_{page_num}.json`.
