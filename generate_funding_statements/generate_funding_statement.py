import csv
import json
import argparse
from local_llm_generate import local_llm_generate
from openai_generate import openai_generate


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate funding statement from templated text.")
    parser.add_argument("-i", "--input_file", type=str,
                        required=True, help="Path to the CSV file.")
    parser.add_argument("-n", "--num_generations", type=int, required=True,
                        help="The number of generated funding statements to return for each input row")
    parser.add_argument(
        "-m", "--model", choices=['local', 'openai'], default='local', help="Model for resolving. Choices: local or openai. Default: local")
    parser.add_argument("-o", "--output_file", type=str,
                        default="generated_statements.csv", help="Path to the output CSV file.")
    return parser.parse_args()


def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def process_data(funding_statement, model):
    with open('prompt.txt', 'r') as file:
        prompt = file.read()
    if model == "local":
        return local_llm_generate(prompt, funding_statement)
    else:
        return openai_generate(prompt, funding_statement)


def main():
    args = parse_arguments()
    num_generations = args.num_generations
    model = args.model
    with open(args.input_file, mode='r', encoding='utf-8') as f_in, open(args.output_file, mode='w', encoding='utf-8') as f_out:
        reader = csv.DictReader(f_in)
        header = reader.fieldnames + ["generated_statement"]
        writer = csv.DictWriter(f_out, fieldnames=header)
        writer.writeheader()
        for row in reader:
            for n in range(num_generations):
                row["generated_statement"] = process_data(
                    row['funding_statement'], model)
                writer.writerow(row)


if __name__ == "__main__":
    main()
