import argparse
import csv


def parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate overlap of 'Funder DOIs-Funder Names' pairs between two CSV files.")
    parser.add_argument('-m', '--matched_file', type=str,
                        required=True, help="Path to the first CSV file.")
    parser.add_argument('-p', '--publisher_asserted_file', type=str,
                        required=True, help="Path to the second CSV file.")
    parser.add_argument('-o', '--output_file', type=str,
                        default='matched_publisher_asserted_overlap.csv', help="Path to the output CSV file.")
    return parser.parse_args()


def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        print(len(data))
    return data


def combine_columns(data):
    return {(row['Funder DOIs'], row['Funder Names']) for row in data}


def find_overlap(matched_pairs, publisher_pairs):
    return matched_pairs.intersection(publisher_pairs)


def write_to_csv(overlap, output_path):
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Funder DOIs', 'Funder Names'])
        for pair in overlap:
            writer.writerow(pair)


def main():
    args = parse_args()
    matched = read_csv(args.matched_file)
    publisher_asserted = read_csv(args.publisher_asserted_file)
    matched_pairs = combine_columns(matched)
    print(len(matched_pairs))
    publisher_asserted_pairs = combine_columns(publisher_asserted)
    overlap = find_overlap(matched_pairs, publisher_asserted_pairs)
    write_to_csv(overlap, args.output_file)
    overlap_count = len(overlap)
    total_count = len(matched_pairs)
    overlap_percentage = (overlap_count / total_count) * 100
    print(f"Overlap Count: {overlap_count} / {total_count}")
    print(f"Overlap Percentage: {overlap_percentage:.2f}%")


if __name__ == "__main__":
    main()
