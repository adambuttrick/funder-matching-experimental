import csv
import argparse
from statistics import mode
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True,
                        type=str, help='Path to the input CSV file.')
    parser.add_argument('-o', '--output_file', default='unique_names.csv', type=str,
                        help='Path to the output CSV file. Default is "unique_names.csv"')
    return parser.parse_args()


def parse_csv(input_file_path):
    with open(input_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def analyze_data(data):
    funder_info = defaultdict(lambda: {"count": 0, "names": set()})
    for row in data:
        doi = row["Funder DOIs"]
        name = row["Funder Names"]
        funder_info[doi]["count"] += 1
        funder_info[doi]["names"].add(name)
    return funder_info


def write_to_csv(funder_info, output_file_path):
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Funder DOI', 'Unique Count', 'Funder Names'])
        for doi, info in funder_info.items():
            names = "; ".join(info["names"])
            writer.writerow([doi, info["count"], names])


def calculate_metrics(funder_info):
    counts = [info["count"] for _, info in funder_info.items()]
    average = sum(counts) / len(counts) if counts else 0
    sorted_counts = sorted(counts)
    mid = len(sorted_counts) // 2
    median = (sorted_counts[mid] + sorted_counts[~mid]) / 2
    mode_value = mode(counts)
    max_count = max(counts)
    initial_step = 10
    threshold = 100
    ranges = {}
    lower_bound = 1
    while lower_bound <= max_count:
        if lower_bound < threshold:
            upper_bound = lower_bound + initial_step - 1
        else:
            upper_bound = 2 * lower_bound - 1
        range_key = f"{lower_bound}-{upper_bound}"
        ranges[range_key] = sum(1 for count in counts if lower_bound <= count <= upper_bound)
        lower_bound = upper_bound + 1
    return average, median, mode_value, ranges




def write_metrics(average, median, mode_value, ranges, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Average", average])
        writer.writerow(["Median", median])
        writer.writerow(["Mode", mode_value])
        for range_value, count in ranges.items():
            writer.writerow([f"Count in Range {range_value}", count])


def main():
    args = parse_args()
    data = parse_csv(args.input_file)
    funder_info = analyze_data(data)
    write_to_csv(funder_info, args.output_file)
    average, median, mode_value, ranges = calculate_metrics(funder_info)
    stats_filename = "metrics_" + args.output_file
    write_metrics(average, median, mode_value,
                  ranges, stats_filename)


if __name__ == "__main__":
    main()
