import csv
import json
import argparse
from collections import defaultdict
from bs4 import BeautifulSoup


def convert_records(funder_file, mapping_file):
    funder_names =  defaultdict(list)
    with open(mapping_file, 'r') as f_in:
        mapped_funder_ids = json.load(f_in)
    with open(funder_file, 'r+') as f_in:
        funder_rdf = f_in.read()
        soup = BeautifulSoup(funder_rdf , "xml")
        concepts = soup.find_all('skos:Concept')
        for concept in concepts:
            funder_id = concept['rdf:about']
            mapped_ror_id = mapped_funder_ids.get(funder_id, None)
            if mapped_ror_id:
                all_names = [concept.find('skosxl:prefLabel').find(
                    'skosxl:Label').find('skosxl:literalForm').text]
                alt_labels = concept.find_all('skosxl:altLabel')
                for alt_label in alt_labels:
                    usage_flag = alt_label.find('fref:usageFlag')
                    if not usage_flag:
                        label_text = alt_label.find('skosxl:Label').find('skosxl:literalForm').text
                        all_names.append(label_text)
                funder_names[mapped_ror_id] += all_names
    return funder_names


def write_to_csv(funder_names, output_file):
    with open(output_file, 'w') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['ror_id', 'label'])
        for key, values in funder_names.items():
            for value in values:
                writer.writerow([key, value])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parses Funder RDF into JSON file for ID lookup view")
    parser.add_argument(
        "-f", "--funder_rdf", help="Funder RDF file path", required=True)
    parser.add_argument(
        "-m", "--mapping_file", help="Mapping file path", required=True)
    parser.add_argument(
        "-o", "--output_file", default='funder_registry_training_data.csv', help="Output file path", required=False)
    return parser.parse_args()


def main():
    args = parse_arguments()
    mapped_funder_names = convert_records(args.funder_rdf, args.mapping_file)
    write_to_csv(mapped_funder_names, args.output_file)


if __name__ == '__main__':
    main()
