import argparse
import csv


def read_csv(csv_file):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def read_txt_file(txt_file):
    with open(txt_file, mode='r', encoding='utf-8') as file:
        return {line.strip() for line in file}


def filter_csv(csv_data, dois):
    return [row for row in csv_data if row['doi'] in dois]


def write_csv(filtered_data, output_file):
    if not filtered_data:
        print("No matching records found.")
        return
    fieldnames = filtered_data[0].keys()
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_data)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Filter CSV file based on DOIs in a text file.")
    parser.add_argument("-c", "--csv_file", required=True,
                        help="Path to the CSV file.")
    parser.add_argument("-t", "--txt_file", required=True,
                        help="Path to the text file containing DOIs.")
    parser.add_argument("-o", "--output_file", default="filtered.csv",
                        help="Path for the output filtered CSV file.")
    return parser.parse_args()


def main():
    args = parse_args()
    csv_data = read_csv(args.csv_file)
    dois = read_txt_file(args.txt_file)
    filtered_data = filter_csv(csv_data, dois)
    write_csv(filtered_data, args.output_file)


if __name__ == "__main__":
    main()
