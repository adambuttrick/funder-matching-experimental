import requests
import json

def get_authors(doi):
    crossref_url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(crossref_url)
        response.raise_for_status()
        data = response.json()
        authors = data['message'].get('author', [])
        authors = [f"{author.get('given', '')} {author.get('family', '')}".strip() for author in authors]
        return '; '.join(authors)
    except requests.exceptions.RequestException as e:
        st.error(f"Error querying Crossref API: {e}")