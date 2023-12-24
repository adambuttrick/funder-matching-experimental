import json
import requests
import streamlit as st
from get_work_from_crossref_api import get_authors
from acknowledgements_to_grants import process_api_response_to_grants_schema
from openai_parse_funding_references import openai_parse_funding_references
from local_parse_funding_references_w_authors_and_projects import local_parse_funding_references


def main():
    st.title('DOI Metadata and Funding Statement to Grant Parser')
    doi = st.text_input('Enter DOI', '')
    funding_statement = st.text_area('Enter Funding Statement', '')
    use_local_parsing = st.checkbox('Local LLM')
    use_ai_parsing = st.checkbox('OpenAI')
    if st.button('Process'):
        if doi:
            authors = get_authors(doi)
            if not authors:
                st.error("No authors found for the provided DOI.")
                return
            if use_local_parsing:
                response =  json.loads(local_parse_funding_references(authors, funding_statement))
                grants = process_api_response_to_grants_schema(response, doi)
            elif use_ai_parsing:
                response =  json.loads(openai_parse_funding_references(authors, funding_statement))
                print(response)
                grants = process_api_response_to_grants_schema(response, doi)
            else:
                st.error("Please select a parsing method.")
                return
            st.subheader("Parsed Results")
            st.json(grants)
        else:
            st.error("Please enter a DOI.")

if __name__ == "__main__":
    main()
