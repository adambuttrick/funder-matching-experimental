import argparse
import csv
import random


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Sample a given number of rows from a CSV file.')
    parser.add_argument('-i', '--input_file', required=True,
                        type=str, help='Path to the input CSV file.')
    parser.add_argument('-s', '--sample_size', required=True,
                        type=int, help='Number of rows to sample from the CSV.')
    parser.add_argument('-o', '--output_file', default='sampled.csv', type=str,
                        help='Path to the output CSV file. If not provided, a default name will be generated.')
    return parser.parse_args()


def sample_csv(input_file, sample_size):
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        header, data = rows[0], rows[1:]
        if sample_size > len(data):
            raise ValueError(
                "Sample size is larger than the number of available rows.")
        sampled_data = random.sample(data, sample_size)
    return [header] + sampled_data


def write_to_csv(rows, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def main():
    args = parse_arguments()
    sampled_rows = sample_csv(args.input_file, args.sample_size)
    output_file = args.output_file
    write_to_csv(sampled_rows, output_file)


if __name__ == "__main__":
    main()
