import json
import logging
import requests

def process_investigators(funding_ref):
    investigators = []
    for author in funding_ref.get('associated_authors', []):
        if author.get('name'):
            investigators.append(create_investigator_entry(author.get('name')))
    return investigators


def process_projects(funding_ref):
    all_projects = set()
    for author in funding_ref.get('associated_authors', []):
        for project in author.get('associated_projects', []):
            all_projects.add(project)
    return all_projects


def create_investigator_entry(author_name):
    return {
        "givenName": author_name.split()[0] if author_name else '',
        "familyName": ' '.join(author_name.split()[1:]) if author_name else '',
        "affiliation": {},
        "orcid": "",
        "role": "investigator"
    }


def create_grant_entry(award_number, funder_name, funder_ror_id, funding_schemes, award_type, doi, projects, investigators):
    grant_entries = []
    for scheme in funding_schemes:
        if projects:
            for project in projects:
                grant_entries.append({
                    "depositor": {
                        "depositor_name": "Crossref",
                        "email_address": None
                    },
                    "award-number": award_number,
                    "award-start-date": None,
                    "project": {
                        "project-title": [{"title-text": project, "lang": None}],
                        "investigators": investigators,
                        "funding": {
                            "funder-name": funder_name,
                            "funder-id": funder_ror_id,
                            "funding-type": award_type if award_type else 'award',
                            "funding-scheme": scheme,
                        },
                        "description": []
                    },
                    "doi_data": {"doi": doi, "resource": ""},
                })
        else:
            grant_entries.append({
                "depositor": {
                    "depositor_name": "Crossref",
                    "email_address": None
                },
                "award-number": award_number,
                "award-start-date": None,
                "project": {
                    "project-title": [],
                    "investigators": investigators,
                    "funding": {
                        "funder-name": funder_name,
                        "funder-id": funder_ror_id,
                        "funding-type": award_type if award_type else 'award',
                        "funding-scheme": scheme,
                    },
                    "description": []
                },
                "doi_data": {"doi": doi, "resource": ""},
            })
    return grant_entries


def query_ror_affiliation(funder_name):
    try:
        url = "https://api.ror.org/organizations"
        params = {"affiliation": funder_name}
        r = requests.get(url, params=params)
        api_response = r.json()
        results = api_response['items']
        if results:
            for result in results:
                if result['chosen']:
                    return result['organization']['id']
        return None
    except Exception as e:
        logging.error(f'Error for query: {funder_name} - {e}')
        return None

def deduplicate_list(l):
    return list(set(l))

def process_api_response_to_grants_schema(json_data, doi):
    if not json_data or 'funding_references' not in json_data:
        return []
    grants_data = []
    for funding_ref in json_data['funding_references']:
        funder_name = funding_ref.get('funder', '')
        if funder_name:
        	funder_ror_id = query_ror_affiliation(funder_name)
        award_type = funding_ref.get('award_type', None)
        funding_identifiers = funding_ref.get('funding_identifier', [None]) or [None]
        funding_identifiers = deduplicate_list(funding_identifiers)
        funding_schemes = funding_ref.get('funding_scheme', [None]) or [None]
        funding_schemes = deduplicate_list(funding_schemes)
        for award_number in funding_identifiers:
            investigators = process_investigators(funding_ref)
            projects = process_projects(funding_ref)
            grants = create_grant_entry(
                award_number, funder_name, funder_ror_id, funding_schemes, award_type, doi, projects, investigators)
            grants_data += grants
    return grants_data