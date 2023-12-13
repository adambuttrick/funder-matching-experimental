import csv
import json
import argparse
import signal
import logging
from time import sleep
from openai_parse_funding_references import openai_parse_funding_references
from local_parse_funding_references_w_authors_and_projects import local_parse_funding_references

logging.basicConfig(level=logging.INFO,
					format='%(asctime)s - %(levelname)s - %(message)s')


def signal_handler(signum, frame):
	raise TimeoutError


def read_csv(file_path):
	data = []
	try:
		with open(file_path, mode='r+', encoding='utf-8-sig') as file:
			reader = csv.DictReader(file)
			for row in reader:
				data.append(
					{'doi': row['doi'], 'funding_statement': row['funding_statement'], 'authors': row['authors']})
	except Exception as e:
		logging.error(f"Error reading CSV file {file_path}: {e}")
		raise
	return data


def process_api_response_to_grants_schema(json_data, doi):
	if not json_data or 'funding_references' not in json_data:
		return []
	grants_data = []
	for funding_ref in json_data['funding_references']:
		funder_name = funding_ref.get('funder', '')
		award_type = funding_ref.get('award_type', None)
		funding_identifiers = funding_ref.get('funding_identifier', [None])
		for award_number in funding_identifiers:
			investigators = process_investigators(funding_ref)
			projects = process_projects(funding_ref)
			grants = create_grant_entry(award_number, funder_name, award_type, doi, projects, investigators)
			grants_data += grants
	return grants_data


def process_investigators(funding_ref):
	investigators = []
	for author in funding_ref.get('associated_authors', []):
		if author.get('name'):
			investigators.append(create_investigator_entry(author.get('name')))
	return investigators


def process_projects(funding_ref):
	all_projects = []
	for author in funding_ref.get('associated_authors', []):
		for project in author.get('associated_projects', []):
			all_projects.append(project)
	return all_projects


def create_investigator_entry(author_name):
	return {
		"givenName": author_name.split()[0] if author_name else '',
		"familyName": ' '.join(author_name.split()[1:]) if author_name else '',
		"affiliation": {},
		"orcid": "",
		"role": "investigator"
	}


def create_grant_entry(award_number, funder_name, award_type, doi, projects, investigators):
	grant_entries = []
	if projects:
		for project in projects:
			grant_entries.append({
				"depositor": {
					"depositor_name": "Crossref",
					"email_address": None
				},
				"award-number": award_number,
				"award-start-date": None,
				"project": {
					"project-title": [{"title-text": project, "lang":None}],
					"investigators": investigators,
					"funding": {
						"funder-name": funder_name,
						"funder-id": None,
						"funding-type": award_type if award_type else 'award',
						"funding-scheme": None,
					},
					"description": []
				},
				"doi_data": {"doi": doi, "resource": ""},
			})
	else:
		grant_entries.append({
				"depositor": {
					"depositor_name": "Crossref",
					"email_address": None
				},
				"award-number": award_number,
				"award-start-date": None,
				"project": {
					"project-title": [],
					"investigators": investigators,
					"funding": {
						"funder-name": funder_name,
						"funder-id": None,
						"funding-type": award_type if award_type else 'award',
						"funding-scheme": None,
					},
					"description": []
				},
				"doi_data": {"doi": doi, "resource": ""},
			})
	return grant_entries


def parse_arguments():
	parser = argparse.ArgumentParser(
		description='Process CSV files for funding information.')
	parser.add_argument('-i', '--input_csv', required=True,
						help='Path to the input CSV file containing funding statements.')
	parser.add_argument('-o', '--output_json', default='grants_data.json',
						help='Path to the output JSON file for grants data.')
	parser.add_argument('-p', '--reference_parser', required=True, choices=[
		'local', 'openai'], help='Specify whether to use "local" or "openai" for funding references parsing.')
	return parser.parse_args()


def main():
	args = parse_arguments()
	csv_data = read_csv(args.input_csv)
	for row in csv_data:
		retry_count = 0
		while retry_count < 2:
			try:
				signal.signal(signal.SIGALRM, signal_handler)
				signal.alarm(60)
				if args.reference_parser == 'openai':
					api_response = json.loads(openai_parse_funding_references(row['authors'], row['funding_statement']))
				else:
					api_response = json.loads(local_parse_funding_references(row['authors'], row['funding_statement']))
				print(api_response)
				if api_response:
					grants_data = process_api_response_to_grants_schema(api_response, row['doi'])
					output_filename = f"{row['doi'].replace('/', '_')}.json"
					with open(output_filename, 'w') as file:
						json.dump({"grants": grants_data}, file, indent=4)
					signal.alarm(0)
				else:
					logging.warning(f"Received null API response for DOI {row['doi']}.")
					break
			except TimeoutError:
				logging.warning(f"Timeout occurred for DOI {row['doi']}. Retrying after 90 seconds...")
				sleep(90)
				retry_count += 1
			except json.JSONDecodeError as e:
				logging.error(f"JSON decoding error for DOI {row['doi']}: {e}")
				break
			except Exception as e:
				logging.error(f"An error occurred for DOI {row['doi']}: {e}")
				break
			else:
				break
		if retry_count == 2:
			logging.error(f"Failed to process DOI {row['doi']} after retrying.")
			break


if __name__ == "__main__":
	main()
