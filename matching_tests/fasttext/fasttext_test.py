import csv
import json
import argparse
import logging
from datetime import datetime
from predictor import Predictor

PREDICTOR = Predictor('models/')
now = datetime.now()
script_start = now.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename=f'{script_start}_ensemble_test.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


def load_mapping(mapping_file):
    with open(mapping_file, 'r') as f_in:
        return json.load(f_in)


def parse_and_query(input_file, mapping, output_file, min_fasttext_probability):
    try:
        with open(input_file, 'r+', encoding='utf-8-sig') as f_in, open(output_file, 'w') as f_out:
            reader = csv.DictReader(f_in)
            fieldnames = reader.fieldnames + \
                ["predicted_ror_id", "prediction_score", "predicted_funder_ids"]
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                funder_name = row['funder_name']
                fasttext_prediction = PREDICTOR.predict_ror_id(
                    funder_name, min_fasttext_probability)
                predicted_ror_id, prediction_score = fasttext_prediction
                predicted_funder_ids = mapping.get(
                    predicted_ror_id, None) if predicted_ror_id else None
                row.update({
                    "predicted_ror_id": predicted_ror_id,
                    "prediction_score": prediction_score,
                    "predicted_funder_ids": predicted_funder_ids
                })
                writer.writerow(row)
    except Exception as e:
        logging.error(f'Error in parse_and_query: {e}')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Return fasttext matches for a given CSV file.')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-m', '--mapping_file',
                        help='Mapping JSON file', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file',
                        default='fasttext_results.csv')
    parser.add_argument(
        '-p', '--min_fasttext_probability', help='min_fasttext_probability level for the fasttext predictor', type=float, default=0.8)
    return parser.parse_args()


def main():
    args = parse_arguments()
    mapping = load_mapping(args.mapping_file)
    parse_and_query(args.input, mapping, args.output,
                    args.min_fasttext_probability)


if __name__ == '__main__':
    main()
