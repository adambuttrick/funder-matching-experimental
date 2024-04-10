## Overview
Converts Label Studio export into a training text file format foruse with the Flair library. 


## Usage
```bash
python label_studio_csv_to_flair_training.py --input my_data.csv --output output_data.txt
```

## Input File
Default Label Studio CSV export format. 


## Output File
The output is a Flair training format text file where each line contains a word from the input text followed by its corresponding label. Words without specific labels are marked with 'O'. Text blocks are new line separated.