import os
import json
import requests

def local_parse_funding_references(authors, funding_statement):
	prompt = """ 
**Task Overview:**
1. **Detailed Entity Recognition:**
	 1.1. Explicitly identify each funding organization and grant program in the text.
	 1.2. Extract all grant or award numbers, ensuring no numeric or alphanumeric identifiers are overlooked.
	 1.3. Clearly connect each funding organization and grant program to its specific identifiers, focusing on their exact placement in the text.
	 1.4. Preserve funding references without specific identifiers.

2. **Author-Project-Funding Linkage:**
	 2.1. Where no authors are explicitly associated with funding or a project (e.g. this study/work/project was supported by), associated ALL authors in the input with the funding.
	 2.2. Verify that you associated associated ALL authors in the input with the funding where no authors are explicitly associated with funding or a project
	 2.3. Where an author is identified directly associate them with specific projects or studies as mentioned.
	 2.4. Accurately map each author to their corresponding funding sources, paying close attention to the proximity and sequence of author names and funding details.
	 2.5. Validate the recognition of author names, ensuring complete accuracy and avoiding misinterpretation of non-author text elements.
	 2.6. Precisely match author initials or abbreviations to full names, cross-referencing with the text for verification.


3. **Enhanced Pattern Recognition for Funding Details:**
	 3.1. Thoroughly extract project/study titles from the acknowledgment text, distinguishing them from any general statements.
	 3.2. Implement a robust review process to confirm that all entities labeled as funding identifiers match known grant or award number formats.

4. **In-Depth Association Analysis:**
	 4.1. Conduct a comprehensive analysis of the acknowledgment text to establish clear relationships between authors, projects, and funding sources.
	 4.2. Utilize both text proximity and logical reasoning to form accurate associations between funding identifiers, authors, and their respective projects or studies.

	 5. **Award Type Identification:**
	 5.1. Determine the type of award from the following predefined list: ["award","contract","crowdfunding","endowment","equipment","facilities","fellowship","grant","loan","other","prize","salary-award","secondment","seed-funding","training-grant"]
	 5.2. Default to "award" where no clear category can be identified.

6. **Output Format:**
   6.1. Format the output as JSON with the structure:
      ```json
      {
        "funding_references": [
          {
            "funder": "{funder name}",
            "award_type": "{award type}",
            "funding_identifier": ["{funding identifier}", "{...}"],
            "associated_authors": [
              {
                "name": "{author name}",
                "associated_projects": ["{project name}", "{...}"]
              },
              {...}
            ]
          },
          {...}
        ]
      }
      ```

7. **Input Processing:**
   7.1. Receive and analyze the list of authors and the funding acknowledgment statement.
   7.2. Parse the input text for entity extraction, author-project association, funding identifier, and award type categorization.

	---

	Now, parse the following funding statement using ALL of the outlined tasks. Return the funder names, identifiers, authors, and associated projects using the following output format:
	```json
      {
        "funding_references": [
          {
            "funder": "{funder name}",
            "award_type": "{award type}",
            "funding_identifier": ["{funding identifier}", "{...}"],
            "associated_authors": [
              {
                "name": "{author name}",
                "associated_projects": ["{project name}", "{...}"]
              },
              {...}
            ]
          },
          {...}
        ]
      }
      ```
Input:
"""
	content = f'{prompt} Authors: "{authors}" | Funding statement: "{funding_statement}"'
	data = {
	"model": "openchat",
	"prompt": content,
	"format": "json",
	"stream": False
	}
	r = requests.post('http://localhost:11434/api/generate', json=data)
	response = r.json()
	print(response['response'])
	return response['response']