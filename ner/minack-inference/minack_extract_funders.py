# adapted from https://github.com/jmelot/SoftwareImpactHackathon2023_InstitutionalOSS/tree/main/resources/ner_text_extraction_pipeline

import os
import re
import csv
import json
import argparse
import requests
import torch
from flair.data import Sentence
from flair.models import SequenceTagger
from multiprocessing.pool import Pool


ROR_URL = "https://api.ror.org/organizations"
MODEL = SequenceTagger.load('kalawinka/flair-ner-acknowledgments')


def extract_organisation_names(text):
    """
    Extract organisation names from text using the Minack Flair NER model.

    :param text: Input text
    :return: List of extracted organisation names
    """
    # Model was trained with funders split into multiple categories,
    # so collapse back into a single group. 
    # See: https://doi.org/10.48550/arXiv.2307.13377 for full details.
    org_tags = ['FUND', 'UNI', 'MISC', 'COR']
    sentence = Sentence(text)
    MODEL.predict(sentence)
    names = {entity.text for entity in sentence.get_spans(
        'ner') if entity.tag in org_tags}
    # GRNB is the tag for award identifiers
    awards = {entity.text for entity in sentence.get_spans(
        'ner') if entity.tag == 'GRNB'}
    return list(names), list(awards)


def get_ror_id(org_name):
    """
    Using ROR's affiliation matching service, map organisation name to ROR ID.

    :param org_name: Organisation name
    :return: ROR ID or None
    """

    # the name has to contain at least one letter
    if org_name is None or not re.search("[a-zA-Z]", org_name):
        return None

    # remove characters that cause ROR API to return 500
    org_name = re.sub('[{."\\\\]', "", org_name)

    matched = requests.get(ROR_URL, {"affiliation": org_name})
    if matched.status_code != 200:
        print(
            f"ROR API request failed; input {org_name}, status code: "
            + f"{matched.status_code}, content: {matched.content}"
        )
        return None
    matched = matched.json()

    for matched_org in matched["items"]:
        if matched_org["chosen"]:
            return matched_org["organization"]["id"]
    return "No match found"


def generate_funding_statements(input_dir):
    """
    Generator of funding_statement objects.

    :param input_dir: Input directory
    :return: A sequence of funding_statement objects
    """
    for f_name in os.listdir(input_dir):
        f_path = os.path.join(input_dir, f_name)
        with open(f_path, "r") as f:
            for line in f:
                yield json.loads(line)


def extract_ror_ids_from_funding_statement(data):
    """
    Extract ROR IDs from a given funding_statement.

    :param data: A tuple containing sequence number and funding_statement.
    :return: A tuple containing the doi, extracted organisation names, award numbers, and ROR IDs
    """
    i, funding_statement = data
    print(f"Processing funding statement #{i} {funding_statement['doi']}")
    org_names, awards = extract_organisation_names(
        funding_statement["content"])
    ror_ids = [get_ror_id(org_name) for org_name in org_names]
    names_awards_ids = [(n, a, r) for n, a, r in zip(
        org_names, awards, ror_ids) if r is not None]
    return funding_statement["doi"], names_awards_ids


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--input", help="input dir path", required=True)
    parser.add_argument("-t", "--threads",
                        help="number of threads", type=int, default=4)
    parser.add_argument(
        "-c", "--chunk", help="imap chunk size", type=int, default=16)
    parser.add_argument(
        "-o", "--output", help="output CSV file", required=True)
    args = parser.parse_args()

    funding_statement_generator = generate_funding_statements(args.input)

    with open(args.output, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["doi", "org_name", "award", "ror_id"])
        with Pool(args.threads) as p:
            args_generator = enumerate(funding_statement_generator)
            for doi, names_awards_ids in p.imap(
                extract_ror_ids_from_funding_statement, args_generator, args.chunk
            ):
                for org_name, award, ror_id in names_awards_ids:
                    writer.writerow([doi, org_name, award, ror_id])
