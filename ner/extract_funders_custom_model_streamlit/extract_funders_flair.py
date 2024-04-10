import re
import requests
from flair.data import Sentence
from flair.models import SequenceTagger

ROR_URL = "https://api.ror.org/organizations"
MODEL_PATH = ''
model = SequenceTagger.load(MODEL_PATH)


def extract_organisation_names(text):
    org_tags = []
    sentence = Sentence(text)
    model.predict(sentence)
    names = {entity.text for entity in sentence.get_spans(
        'ner') if entity.tag == 'ORG'}
    return list(names)


def get_ror_id(org_name):
    if org_name is None or not re.search("[a-zA-Z]", org_name):
        return None
    org_name = re.sub('[{."\\\]', "", org_name)
    matched = requests.get(ROR_URL, {"affiliation": org_name})
    if matched.status_code != 200:
        return None
    matched = matched.json()
    for matched_org in matched["items"]:
        if matched_org["chosen"]:
            return matched_org["organization"]["id"]
    return None


def extract_funders_and_ror_ids(text):
    org_names = extract_organisation_names(text)
    ror_ids = [get_ror_id(org_name) for org_name in org_names]
    names_awards_ids = []
    for org_name, ror_id in zip(org_names, ror_ids):
        names_awards_ids.append((org_name, ror_id))
    return names_awards_ids
