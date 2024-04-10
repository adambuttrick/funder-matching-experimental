import csv
import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert annotated CSV to text format')
    parser.add_argument('-i','--input', required=True, help='Input CSV file path')
    parser.add_argument('-o','--output', default='train.txt',
                        help='Output text file path')
    return parser.parse_args()


def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        print(reader.fieldnames)
        data = [(row['text'], row['label']) for row in reader]
    return data


def parse_annotations(text, label_data):
    annotations = json.loads(label_data)
    print(annotations)
    words = text.split()
    labels = ['O'] * len(words)
    for annotation in annotations:
        start_index = annotation['start']
        end_index = annotation['end']
        label = annotation['labels'][0]
        word_index = text.count(' ', 0, start_index)
        end_word_index = text.count(' ', 0, end_index)
        for i in range(word_index, end_word_index + 1):
            labels[i] = label
    return list(zip(words, labels))


def generate_output(pairs):
    return '\n'.join([f'{word} {label}' for word, label in pairs])


def write_output(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    args = parse_args()
    data = read_csv(args.input)
    output_lines = []
    for text, label_data in data:
        pairs = parse_annotations(text, label_data)
        output_lines.append(generate_output(pairs))
    final_output = '\n\n'.join(output_lines)
    write_output(args.output, final_output)


if __name__ == "__main__":
    main()
