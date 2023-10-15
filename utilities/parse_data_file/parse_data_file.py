import argparse
import json
import csv
import os
import glob
import gzip
import chardet


def get_all_json_files(directory):
    return glob.glob(os.path.join(directory, "*.json.gz"))


def detect_encoding(byte_data):
    return chardet.detect(byte_data)['encoding']


def decode_data(byte_data, assumed_encoding='utf-8'):
    try:
        return byte_data.decode(assumed_encoding)
    except UnicodeDecodeError:
        return byte_data.decode(detect_encoding(byte_data))


def extract_data_from_json(json_path):
    with gzip.open(json_path, 'rb') as json_file:
        byte_data = json_file.read()
        decoded_data = decode_data(byte_data)
        data = json.loads(decoded_data)

    extracted_data = []
    for item in data["items"]:
        doi = item.get("DOI", "")
        creation_date = item.get("created", {}).get("date-time", "")
        publication_date = item.get("published", {}).get(
            "date-parts", [[""]])[0][0]
        funders = item.get("funder", [])
        if funders:
            for funder in funders:
                funder_doi = funder.get("DOI", "")
                funder_name = funder.get("name", "")
                doi_asserted_by = funder.get("doi-asserted-by", "")
            extracted_data.append([doi, creation_date, publication_date,
                                   funder_doi, funder_name, doi_asserted_by])
    return extracted_data


def deduplicate_data(data):
    seen = set()
    unique_data = []
    for item in data:
        tuple_item = tuple(item)
        if tuple_item not in seen:
            seen.add(tuple_item)
            unique_data.append(item)
    return unique_data


def write_data_to_csv(data, csv_path):
    headers = ["DOI", "Creation Date", "Publication Date",
               "Funder DOIs", "Funder Names", "DOI Asserted By"]
    with open(csv_path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(data)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert JSON files from a directory into a single CSV file.")
    parser.add_argument("-d", "--directory", type=str,
                        required=True, help="Directory containing JSON files.")
    parser.add_argument("-o", "--output_csv", type=str,
                        default='works.csv', help="Path to save the generated CSV file.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    all_json_files = get_all_json_files(args.directory)
    all_data = []
    for json_file in all_json_files:
        all_data.extend(extract_data_from_json(json_file))
    deduplicated_data = deduplicate_data(all_data)
    write_data_to_csv(deduplicated_data, args.output_csv)


if __name__ == "__main__":
    main()
