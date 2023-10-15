import os
import csv
import argparse
from collections import defaultdict


def read_data_from_csv(csv_path):
    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
    return data


def count_doi_asserted_by_values(data):
    counts = defaultdict(int)
    total = 0
    for row in data:
        doi_asserted_by = row.get("DOI Asserted By", "").strip()
        counts[doi_asserted_by] += 1
        total += 1
    percentages = {key: (value / total) * 100 for key, value in counts.items()}
    return counts, percentages


def filter_and_write_csv(data, output_dir, input_file_name, filter_value):
    headers = list(data[0].keys())
    filtered_data = [row for row in data if row.get(
        "DOI Asserted By", "").strip() == filter_value]

    if not filter_value:
        file_name = f"{output_dir}/{input_file_name}_funder_asserted_by_null.csv"
    else:
        file_name = f"{output_dir}/{input_file_name}_funder_asserted_by_{filter_value}.csv"

    with open(file_name, "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        for row in filtered_data:
            writer.writerow(row)


def write_summary_file(counts, percentages, output_dir, input_file_name):
    summary_file_name = f"{output_dir}/{input_file_name}_funder_assertion_metrics.csv"
    with open(summary_file_name, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["DOI Asserted By", "Count", "Percentage"])
        for key, value in counts.items():
            writer.writerow([key, value, f"{percentages[key]:.2f}%"])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate files based on 'DOI Asserted By' values and a summary metrics CSV.")
    parser.add_argument("-i", "--input_csv",
                        help="Input CSV file path.", required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    data = read_data_from_csv(args.input_csv)
    counts, percentages = count_doi_asserted_by_values(data)
    output_dir = os.path.dirname(args.input_csv)
    input_file_name = os.path.basename(args.input_csv).split('.')[
        0]
    for key in counts.keys():
        filter_and_write_csv(data, output_dir, input_file_name, key)
    write_summary_file(counts, percentages, output_dir, input_file_name)


if __name__ == "__main__":
    main()
