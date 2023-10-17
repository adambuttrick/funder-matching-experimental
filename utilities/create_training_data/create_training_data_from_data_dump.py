import re
import csv
import sys
import json
import argparse
import unicodedata
from unidecode import unidecode


# Used to remove (Country Name) from the primary name field, as is included on
# some records to distinguish national-level branches of various organizations
def preprocess_primary_name(name):
    name = re.sub(r'\s\(.*\)', '', name)
    return name


# Only labels are tagged with languages, so this check is needed to exclude
# aliases and acronyms with non-Latin characters from the faked affiliations
# (non-Latin character names require discrete prep and training approaches
# from their Latin character counterparts).
def check_latin_chars(s):
    for ch in s:
        if ch.isalpha():
            if 'LATIN' not in unicodedata.name(ch):
                return False
    return True


# Add whatever other normalization you want here. Keeping things conservative for now.
def normalize_text(s):
    return unidecode(re.sub(r'\s+', ' ', s))


# Return labels for records with a single parent to form a compound affiliation with
# their parents
def find_parent_label(dicts):
    parent_dicts = [d for d in dicts if d["type"] == "Parent"]
    if len(parent_dicts) == 1:
        return parent_dicts[0]["label"]
    else:
        return None


# Utility function to extract and process values from record
def get_record_value(record, key, process_func=None):
    val = record.get(key, [])
    if process_func:
        val = [process_func(v) for v in val]
    return val


def get_record_name(record, key):
    return get_record_value(record, key, process_func=lambda x: x.get('label'))


def get_all_names(record):
    funder_ids = []
    primary_name = preprocess_primary_name(record.get('name', ''))
    aliases = get_record_value(record, 'aliases')
    labels = get_record_name(record, 'labels')
    acronyms = get_record_value(record, 'acronyms')
    all_names = [primary_name] + aliases + labels + acronyms
    all_names = [normalize_text(name)
                 for name in all_names if check_latin_chars(name)]
    external_ids = record['external_ids']
    return all_names


# See https://zenodo.org/communities/ror-data/ for the latest data dump
def data_dump_to_training_data(data_dump_file, output_file):
    training_data = {}
    with open(data_dump_file, 'r+') as f_in:
        ror_records = json.load(f_in)
        for record in ror_records:
            if record['status'] != 'withdrawn':
                ror_id = record['id']
                training_data[ror_id] = get_all_names(record)
    with open(output_file, 'w') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['ror_id', 'label'])
        for key, values in training_data.items():
            for value in values:
                writer.writerow([key, value])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate fake affiliation training data from the ROR data dump file.')
    parser.add_argument(
        '-i', '--input', help='ROR data dump file', required=True)
    parser.add_argument(
        '-o', '--output', help='Output CSV file', default='ror_data_dump_training_data.csv')
    return parser.parse_args()


def main():
    args = parse_arguments()
    data_dump_to_training_data(args.input, args.output)


if __name__ == '__main__':
    main()
