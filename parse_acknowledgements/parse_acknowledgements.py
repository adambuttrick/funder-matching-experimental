import os
import csv
import json
import argparse
import signal
import logging
from time import sleep, time
from openai_parse_funding_references import openai_parse_funding_references
from local_parse_funding_references import local_parse_funding_references

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def signal_handler(signum, frame):
    raise TimeoutError


def read_csv(file_path):
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(
                    {'doi': row['doi'], 'funding_statement': row['funding_statement']})
    except Exception as e:
        logging.error(f"Error reading CSV file {file_path}: {e}")
        raise
    return data


def parse_json_and_prepare_csv_data(json_data, doi, funding_statement):
    prepared_data = []
    if json_data and 'funding_references' in json_data:
        for funding_ref in json_data['funding_references']:
            funder = funding_ref.get('funder', '')
            funding_identifiers = funding_ref.get('funding_identifier', [])
            if not funding_identifiers:
                prepared_data.append({
                    'doi': doi,
                    'funding_statement': funding_statement,
                    'funder': funder,
                    'funding_identifier': None
                })
            else:
                for identifier in funding_identifiers:
                    prepared_data.append({
                        'doi': doi,
                        'funding_statement': funding_statement,
                        'funder': funder,
                        'funding_identifier': identifier
                    })
    return prepared_data


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Process CSV files for funding information.')
    parser.add_argument('-i', '--input_csv', required=True,
                        help='Path to the input CSV file containing funding statements.')
    parser.add_argument('-o', '--output_csv', default='funding_references.csv',
                        help='Path to the output CSV file for funding references csv.')
    parser.add_argument('-p', '--reference_parser', required=True, choices=[
                        'local', 'openai'], help='Specify whether to use: "local" or "openai" for funding references parsing.')
    return parser.parse_args()


def main():
    args = parse_arguments()
    csv_data = read_csv(args.input_csv)
    with open(args.output_csv, mode='w', newline='', encoding='utf-8') as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=[
                                    'doi', 'funding_statement', 'funder', 'funding_identifier'])
        csv_writer.writeheader()
        for row in csv_data:
            retry_count = 0
            while retry_count < 2:
                try:
                    signal.signal(signal.SIGALRM, signal_handler)
                    signal.alarm(60)
                    if args.reference_parser == 'openai':
                        api_response = json.loads(
                            openai_parse_funding_references(row['funding_statement']))
                    else:
                        api_response = json.loads(
                            local_parse_funding_references(row['funding_statement']))
                    if api_response:
                        prepared_data = parse_json_and_prepare_csv_data(
                            api_response, row['doi'], row['funding_statement'])
                        csv_writer.writerows(prepared_data)
                        signal.alarm(0)
                    else:
                        logging.warning(f"Received null API response.")
                        break
                except TimeoutError:
                    logging.warning(f"Timeout occurred for DOI {row['doi']}. Retrying after 90 seconds...")
                    sleep(90)
                    retry_count += 1
                except json.JSONDecodeError as e:
                    logging.error(f"JSON decoding error for DOI {row['doi']}: {e}")
                    break
                else:
                    break
            if retry_count == 2:
                logging.error(f"Failed to process DOI {row['doi']} after retrying.")
                break


if __name__ == "__main__":
    main()
