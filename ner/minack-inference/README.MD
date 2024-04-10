## Overview
Extracts organization names and award numbers from text data using the [MinAck NER model](https://kalawinka.github.io/minack/) and maps these names to their respective ROR IDs using the ROR API.

## Requirements
- Python 3
- Libraries: os, re, csv, json, argparse, requests, torch, flair, multiprocessing

## Installation
Ensure Python 3 and pip are installed. Install dependencies:
```
pip install requests torch flair
```

## Usage
```
python minack_extract_funders.py -f INPUT_DIR -o OUTPUT_FILE [-t THREADS] [-c CHUNK_SIZE]
```
- `-f/--input`: Path to the input directory containing funding statements in JSONL format.
- `-o/--output`: Path to the output CSV file.
- `-t/--threads`: Optional. Number of threads to use (default: 4).
- `-c/--chunk`: Optional. imap chunk size (default: 16).

## Input Format
The input directory should contain work metadata and funding statements in JSON format. See test data for an example. 

## Output Format
The script outputs a CSV file with columns: DOI, Organization Name, Award Number, ROR ID.
