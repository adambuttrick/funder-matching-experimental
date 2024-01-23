import re
import csv
import sys
import argparse
import unicodedata
import itertools
import regex as re


# To make sure we the model can be trained to parse multiple funders, we set a lower bound of asserted
# funders, which is used to filter the training data
DEFAULT_FUNDER_COUNT = 3


def preprocess_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def index_substring(substring, text):
    if not substring:
        return None
    preprocessed_substring = preprocess_text(substring)
    if not preprocessed_substring:
        return None
    preprocessed_text = preprocess_text(text)
    start_index = preprocessed_text.find(preprocessed_substring)
    if start_index != -1:
        end_index = start_index + len(preprocessed_substring)
        if end_index > start_index:
            return [start_index, end_index, preprocessed_text[start_index:end_index]]
    return None


def process_funder_csv(funder_csv):
    funders_data = {}
    with open(funder_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            doi = row['DOI']
            if doi not in funders_data:
                funders_data[doi] = {'funders': [], 'awards': []}
            funders_data[doi]['funders'].append(row['Funder Name'])
            funders_data[doi]['awards'].extend(row['Awards'].split(";"))
    return funders_data


def process_publication_csv(publication_csv):
    with open(publication_csv, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def verify_and_index_funder_information(funders_data, publications, output_file):
    output_rows = []
    processed_indexes = {}
    for pub in publications:
        doi = pub['doi']
        funding_info = pub['funding-information']
        # Some funding statements have random, pernicious junk characters, so drop from training data
        if not any([ch.isprintable() == False for ch in funding_info]):
            if doi in funders_data:
                funders_extracted = []
                awards_extracted = []
                if doi not in processed_indexes:
                    processed_indexes[doi] = set()
                for funder in funders_data[doi]['funders']:
                    funder_index = index_substring(funder, funding_info)
                    if funder_index and funder_index[0] not in processed_indexes[doi]:
                        processed_indexes[doi].add(funder_index[0])
                        funders_extracted.append({
                            'doi': doi,
                            'text': funding_info,
                            'start_index': funder_index[0],
                            'stop_index': funder_index[1],
                            'index_substring': funder_index[2],
                            'type': 'funder'
                        })
                for award in funders_data[doi]['awards']:
                    award_index = index_substring(award, funding_info)
                    if award_index and award_index[0] not in processed_indexes[doi]:
                        processed_indexes[doi].add(award_index[0])
                        awards_extracted.append({
                            'doi': doi,
                            'text': funding_info,
                            'start_index': award_index[0],
                            'stop_index': award_index[1],
                            'index_substring': award_index[2],
                            'type': 'award'
                        })
                if len(funders_extracted) >= DEFAULT_FUNDER_COUNT and \
                   len(funders_extracted) == len(funders_data[doi]['funders']) and \
                   len(awards_extracted) == len(funders_data[doi]['awards']):
                    output_rows.extend(funders_extracted)
                    output_rows.extend(awards_extracted)

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'doi', 'text', 'start_index', 'stop_index', 'index_substring', 'type'])
        writer.writeheader()
        writer.writerows(output_rows)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Funder Information Verification and Indexing System')
    parser.add_argument('-f', '--funder_csv', required=True,
                        help='Funder CSV file path')
    parser.add_argument('-p', '--publication_csv',
                        required=True, help='Publication CSV file path')
    parser.add_argument('-o', '--output', default='filtered_ner_indexes_funding_statements.csv',
                        help='Output CSV file path')
    return parser.parse_args()


def main():
    args = parse_args()
    funders_data = process_funder_csv(args.funder_csv)
    publications = process_publication_csv(args.publication_csv)
    verify_and_index_funder_information(
        funders_data, publications, args.output)


if __name__ == '__main__':
    main()
