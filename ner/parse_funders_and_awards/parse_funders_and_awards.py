import argparse
import csv
import json
import os
import gzip
import glob
import chardet
from multiprocessing.pool import Pool


def get_all_json_files(directory):
    return glob.glob(os.path.join(directory, "*.json.gz"))


def detect_encoding(byte_data):
    return chardet.detect(byte_data)['encoding']


def decode_data(byte_data, assumed_encoding='utf-8'):
    try:
        return byte_data.decode(assumed_encoding)
    except UnicodeDecodeError:
        return byte_data.decode(detect_encoding(byte_data))


def process_json_file(json_path):
    try:
        with gzip.open(json_path, 'rb') as json_file:
            byte_data = json_file.read()
            decoded_data = decode_data(byte_data)
            data = json.loads(decoded_data)
        extracted_data = []
        for item in data["items"]:
            doi = item.get("DOI", "")
            funders = item.get("funder", [])
            for funder in funders:
                funder_doi = funder.get("DOI", "")
                funder_name = funder.get("name", "")
                awards = funder.get("award", None)
                if awards:
                    if len(awards) > 1:
                        awards = '; '.join(awards)
                    else:
                        awards = awards[0]
                extracted_data.append([doi, funder_doi, funder_name, awards])
        return extracted_data
    except Exception as e:
        print(f"Error processing file {json_path}: {e}")
        return []


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", required=True,
                        help="Directory containing JSON files.")
    parser.add_argument("-o", "--output_csv", default='all_funders_and_awards.csv',
                        help="Path for the output CSV file.")
    parser.add_argument("-t", "--threads", type=int,
                        default=4, help="Number of threads to use.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    all_json_files = get_all_json_files(args.directory)
    with open(args.output_csv, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["DOI", "Funder DOI", "Funder Name", "Awards"])
        with Pool(args.threads) as pool:
            args_generator = (json_file for json_file in all_json_files)
            for result in pool.imap(process_json_file, args_generator):
                for record in result:
                    writer.writerow(record)


if __name__ == "__main__":
    main()
