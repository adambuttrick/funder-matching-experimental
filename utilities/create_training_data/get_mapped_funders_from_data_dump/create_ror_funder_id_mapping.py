import json
import argparse


def create_mapping_and_output_json(ror_data_file, json_output_file):
    mapping = {}
    with open(ror_data_file, 'r+') as f_in:
        ror_data = json.load(f_in)
    for item in ror_data:
        ror_id = item.get('id', None)
        funder_ids = item.get('external_ids', {}).get('FundRef', {}).get('all', [])
        if funder_ids:
            funder_ids = [f'http://dx.doi.org/10.13039/{funder_id}' for funder_id in funder_ids]
            funder_ids = list(set(funder_ids))
            for funder_id in funder_ids:
                mapping[funder_id] = ror_id
    with open(json_output_file, 'w') as json_file:
        json.dump(mapping, json_file)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate ROR-Funder ID mapping from the ROR data dump file.')
    parser.add_argument(
        '-d', '--data_dump', help='ROR data dump file', required=True)
    parser.add_argument(
        '-o', '--output_file', help='Output JSON file', default='ror-funder_mapping.json ')
    return parser.parse_args()


def main():
    args = parse_arguments()
    create_mapping_and_output_json(args.data_dump, args.output_file)


if __name__ == "__main__":
    main()
