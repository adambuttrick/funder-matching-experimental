import os
import json
import requests

def local_parse_funding_references(funding_statement):
	prompt = '''You are tasked with developing a named entity recognition dataset specifically tailored for identifying and classifying funding-related entities in text. This task involves meticulously scanning input text to label entities that represent funding organizations and their respective funding identifiers, such as grant IDs or award numbers. It is crucial to accurately discern these specific types of entities while excluding irrelevant ones. To enhance the precision of your dataset, you will employ pattern matching techniques to identify potential misclassifications and prune extraneous text from the identified entities. This process requires a keen eye for detail and an understanding of the common formats and structures of funding identifiers and organization names. Your ultimate goal is to produce a structured dataset with clearly defined entities that can be readily used for advanced text analysis and data extraction purposes.

**Task Overview:**
**Entity Identification:**
1.1. Scan the input text for organization names and funding identifiers (e.g., grant IDs, award numbers).
1.2. Ensure identified entities are not parts of speech but actual organization names or funding identifiers.

**Pattern Matching for Funding Identifiers:**
2.1. Develop a pattern matching method for funding identifiers.
2.2. Identify common patterns in funding identifiers, such as starting with a digit followed by a letter (e.g., "3P", "5P", "5R").
2.3. Flag any entity labeled as a funding identifier that does not match the identified pattern for review.

**Pruning Extraneous Text:**
3.1. **Identify and Isolate Funding Identifiers:**
	- Isolate specific segments of text explicitly labeled as funding identifiers, typically following labels like "No." or similar designations.
3.2. **Exclude Unrelated Information:**
	- Remove parts of the text that do not contribute to the identification of the funding source, including personal acknowledgments, descriptive phrases about roles or contributions, and extraneous words or symbols.
3.3. **Pattern Matching for Identifier Validation:**
	- Apply pattern matching to validate the structure of funding identifiers. Flag any segment not matching this pattern for review.
3.4. **Handling Ambiguous Cases:**
	- Flag segments for manual review when it's unclear whether they are part of the funding identifier or extraneous information.
3.5. **Final Formatting:**
	- Ensure the remaining text for each funding identifier is concise and limited to essential components, transforming phrases like "No. ABC123, funded by XYZ" to just "No. ABC123".
3.6. **Review and Confirmation:**
	- Conduct a final review of the pruned identifiers to confirm their accuracy and completeness.

**Review Flagged Entities:**
4.1. Manually review entities flagged in steps 2.3 and 3.4.
4.2. Confirm if flagged entities are actual funding identifiers or other parts of text.

**Discard Non-Funding Identifiers:**
5.1. Remove all values from the dataset that are not funding identifiers.

**Output Format:**
6.1. Format the output as JSON with the structure:
   ```
   {
	 "funding_references": [
	   {
		 "funder": "{funder name}",
		 "funding_identifier": [
		   {funding identifier},
		   {...}
		 ]
	   },
	   {...}
	 ]
   }
   ```
6.2. Ensure each funder entity and its associated funding identifiers are correctly listed.

**Input Processing:**
7.1. Receive and process input text according to the above steps.
7.2. Ensure the input text is adequately parsed for entity extraction and processing.

---

Now, parse the following funding statement using ALL of the outlined tasks. Return the funder names and identifiers using the following output format. Output format:{"funding_references:" [{"funder": "{funder name}", "funding_identifier":["{funding identifier}","{...}"]}, "{...}"]}. Input:'''
	content = prompt + funding_statement
	data = {
	"model": "mistral-openorca",
	"prompt": content,
	"format": "json",
	"stream": False
	}
	r = requests.post('http://localhost:11434/api/generate', json=data)
	response = r.json()
	return response['response']