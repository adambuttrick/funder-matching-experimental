import os
import sys
import time
import json
import argparse
import requests

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start_date", type=str, required=True)
    parser.add_argument("-e", "--end-date", type=str, required=True)
    parser.add_argument('-u', '--user_agent', type=str,
                        help='User Agent for the request (mailto:name@email)')
    parser.add_argument("-t", "--token", type=str,
                        help='Crossref Metadata Plus API token')
    return parser.parse_args()


def retry_request(url, headers, params):
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed due to: {str(e)}. Retrying in 30 seconds.")
            time.sleep(30)
    return None


def download_json(start_date, stop_date, headers, rows=1000):
    BASE_URL = "https://api.crossref.org/works"
    directory_name = f"{start_date}_{stop_date}_works_w_funding_assertions"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    cursor = '*'
    page_num = 1
    while True:
        response = retry_request(BASE_URL, headers, {
            "filter": f"from-pub-date:{start_date},until-pub-date:{stop_date},has-funder:t", 
            "cursor": cursor,
            "rows": rows
        })
        if response is None:
            print(f"Failed to retrieve data for funder {funder_id} after 3 attempts.")
            sys.exit(1)
        items = response.json().get('message', {}).get('items',[])
        if not items:
            break
        with open(f"{directory_name}/{start_date}-{stop_date}_page_{page_num}.json", "w") as file:
            json.dump(response.json(), file)
        cursor = response.json().get('message', {}).get('next-cursor', None)
        if not cursor:
            break
        page_num += 1
        time.sleep(5)


def main():
    args = parse_arguments()
    headers = {}
    if args.token:
        headers['Crossref-Plus-API-Token'] = args.token
    if args.user_agent:
        headers['User-Agent'] = args.user_agent
    download_json(args.start_date, args.end_date, headers)


if __name__ == "__main__":
    main()
