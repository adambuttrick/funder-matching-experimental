import string
import csv
import argparse


def read_input_file(input_file):
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def tokenize_text(text):
    tokens = []
    word_start_index = 0
    for word_end_index in range(len(text)):
        if text[word_end_index] in [" ", "\n"] or word_end_index == len(text) - 1:
            word = text[word_start_index:word_end_index] if text[
                word_end_index] == " " else text[word_start_index:word_end_index+1]
            tokens.append((word, word_start_index, word_end_index))
            word_start_index = word_end_index + 1
    return tokens


def tag_words(tokens, entities, start_tag, inside_tag, default_tag='O'):
    tags = [default_tag] * len(tokens)
    for entity in entities:
        start_index = int(entity['start_index'])
        stop_index = int(entity['stop_index'])
        for i, (word, word_start, word_end) in enumerate(tokens):
            if word_start == start_index:
                if tags[i] == default_tag:
                    tags[i] = start_tag
            elif word_start > start_index and word_end <= stop_index:
                if tags[i] == default_tag:
                    tags[i] = inside_tag
    return tags


def remove_leading_trailing_punctuation(text):
    if text[0] in string.punctuation:
        text = text[1:]
    if len(text) <= 3:
        return text
    i = 1
    while i <= 3 and text[-i] in string.punctuation:
        i += 1
    return text[:-i + 1] if i > 1 else text


def process_data(data):
    grouped_data = {}
    for row in data:
        key = (row['doi'], row['text'])
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(row)
    lines = []
    for key, group in grouped_data.items():
        funders = [entity for entity in group if entity['type'] == 'funder']
        awards = [
            entity for entity in group if entity['type'] == 'award']
        tokens = tokenize_text(key[1])
        org_tags = tag_words(
            tokens, funders, start_tag='B-ORG', inside_tag='I-ORG')
        identifier_tags = tag_words(
            tokens, awards, start_tag='B-AWARD', inside_tag='I-AWARD')
        final_tags = [org if org != 'O' else identifier for org,
                      identifier in zip(org_tags, identifier_tags)]
        if 'B-ORG' not in final_tags and 'I-ORG' not in final_tags:
            continue
        for i, (word, _, _) in enumerate(tokens):
            word = remove_leading_trailing_punctuation(word)
            line = f"{word} {final_tags[i]}"
            lines.append(line)
        lines.append('')
    return lines


def write_to_text_file(lines, output_file):
    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line + '\n')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Transform a CSV file to tag affiliation strings.")
    parser.add_argument("-i", "--input_file", required=True,
                        help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_file", required=True,
                        help="Path to the output text file.")
    return parser.parse_args()


def main(input_file, output_file):
    data = read_input_file(input_file)
    lines = process_data(data)
    write_to_text_file(lines, output_file)
    print("The data was successfully transformed and written to the output file.")


if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)
