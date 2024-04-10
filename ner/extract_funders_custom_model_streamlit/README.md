# Funder Extraction App

Extract funder names and their corresponding ROR IDs from a given funding statement. Utilizes a custom trained model from the [Flair library](https://github.com/flairNLP/flair?tab=readme-ov-file) for named entity recognition (NER) to identify organization names and the ROR API to retrieve the associated ROR IDs.

## Installation

1. Install the required dependencies from the requirements.txt:

   ```
   pip install -r requirements.txt
   ```

2. Download the trained Flair NER model from [https://huggingface.co/adambuttrick/flair-funder-ner-model-50-epoch](https://huggingface.co/adambuttrick/flair-funder-ner-model-50-epoch).

3. Update the `MODEL_PATH` variable in `extract_funders_flair.py` with the path to the downloaded model:

   ```python
   MODEL_PATH = 'path/to/flair-funder-ner-model-50-epoch'
   ```

## Usage

1. Run the Streamlit app:

   ```
   streamlit run app.py
   ```

2. Access the app in your browser at `http://localhost:8501`

3. Enter a funding statement in the text box.

4. Click the "Extract" button to extract funder names and ROR IDs.

5. The extracted funders and their ROR IDs will be displayed in a table.
