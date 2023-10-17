import csv
import json
import argparse


def load_csv(filepath):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def extract_funders_from_json(json_data):
    funders_set = set()
    for record in json_data:
        if record['status'] != 'withdrawn' and 'FundRef' in record.get('external_ids', {}):
            funders_set.update(record['external_ids']['FundRef']['all'])
    return funders_set


def process_funder_id(funder_id):
    return funder_id.replace("http://dx.doi.org/10.13039/", "")


def split_mapped(csv_data, funders_set):
    mapped = []
    for row in csv_data:
        funder_id = process_funder_id(row['funder_id'])
        if funder_id in funders_set:
            mapped.append(row)
    return mapped


def export_to_csv(data, filepath):
    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Map and divide funders based on JSON data.")
    parser.add_argument("-i", "--input_file", required=True,
                        help="Path to input CSV file.")
    parser.add_argument("-o", "--output_file", default='mapped.csv',
                    help="Path to output CSV file.")
    parser.add_argument("-d", "--data_dump", required=True,
                        help="Path to input JSON file.")
    return parser.parse_args()


def main():
    args = parse_arguments()

    csv_data = load_csv(args.input_file)
    json_data = load_json(args.data_dump)
    funders_set = extract_funders_from_json(json_data)

    mapped= split_mapped(csv_data, funders_set)
    export_to_csv(mapped, args.output_file)


if __name__ == "__main__":
    main()
