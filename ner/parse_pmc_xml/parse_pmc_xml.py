import argparse
import csv
import glob
import os
import multiprocessing
from bs4 import BeautifulSoup


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Parse XML files for DOI, acknowledgements, and funding information.')
    parser.add_argument('-d', '--directory', required=True,
                        help='Directory containing XML files.')
    parser.add_argument('-o', '--output_csv',
                        default='parsed_xml.csv', help='Output CSV file path.')
    parser.add_argument('-t', '--threads', type=int,
                        default=9, help='Number of threads to use.')
    return parser.parse_args()


def get_xml_files(directory):
    return glob.glob(os.path.join(directory, '*.xml'))


def parse_xml(file_path):
    try:
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'xml')
            doi = soup.find('article-id', {'pub-id-type': 'doi'}).get_text(
            ) if soup.find('article-id', {'pub-id-type': 'doi'}) else None
            ack = soup.find('ack')
            ack_text = ack.find('p').get_text(
            ) if ack and ack.find('p') else None
            funding_info = soup.find('funding-statement')
            if funding_info:
                funding_text = funding_info.get_text(strip=True)
            else:
                funding_text = None
                for title in soup.find_all('title'):
                    if title.string and 'funding' in title.string.lower():
                        p_tag = title.find_next_sibling('p')
                        if p_tag:
                            funding_text = p_tag.get_text(strip=True)
                            break
            return [doi, ack_text, funding_text] if doi and (ack_text or funding_text) else None
    except Exception as e:
        print(f'Error processing {file_path}: {e}')
        return None


def main():
    args = parse_arguments()
    xml_files = get_xml_files(args.directory)
    with open(args.output_csv, 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['doi', 'acknowledgements', 'funding-information'])
        with multiprocessing.Pool(args.threads) as pool:
            for result in pool.imap(parse_xml, xml_files):
                if result:
                    writer.writerow(result)


if __name__ == '__main__':
    main()
