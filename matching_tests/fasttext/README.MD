# fastext_test
Return fasttext matches matches for a given CSV file and compare to assigned ROR IDs.

## setup
````
pip install -r requirements.txt
````
[Download the model files from Hugging Face](https://huggingface.co/poodledude/ror-predictor/tree/main) and place in a directory called  "models."

## usage
Prepare a CSV file containing funder name strings and assigned ROR IDs. Label the funder name string column "funder name."

Run the script with the required arguments:
````
$ python fastext_test.py -i <input_file> [-o <output_file>] [-c <confidence_level>]
````
