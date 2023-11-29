import os
from openai import OpenAI

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']
)

def openai_parse_funding_references(funding_statement):
	schema = {
		"type": "object",
		"properties": {
			"funding_references": {
				"type": "array",
				"items": {
					"type": "object",
					"properties": {
						"funder": {
							"type": "string"
						},
						"funding_identifier": {
							"type": "array",
							"items": {
								"type": "string"
							}
						},
					},
					"required": ["funder", "funding_identifier"]
				}
			}
		},
		"required": ["funding_references"]
	}

	prompt = """ 
The goal is to create a dataset for named entity recognition. Label as many funder entities and funding identifiers entities as possible in the input text. Make sure the entity concept is not part of speech but an organization name or funding identifier, such as a grant ID or award number. Avoid finding entities other than organizations and funding identifiers. Develop a pattern matching method to identify potential misclassifications of funding identifiers. For example, grant numbers often start with a digit followed by a letter (e.g., '3P', '5P', '5R') and continue with more alphanumeric characters. If an entity labeled as a funding identifier does not match this pattern, flag it for review. Once flagged entities are reviewed, confirmed whether they are funding identifiers or other pars of text. Discard any values that are not funding identifiers. Output format:
{"funding_references: [{"funder": "{funder name}", "funding_identifier":[{funding identifier},{...}]}, {...}]}. Input:
"""
	content = prompt + funding_statement
	try:
		response = client.chat.completions.create(
			model = "gpt-3.5-turbo",
			messages = [
				{"role": "system", "content": "You are a named-entity recognition agent tasked with extracting the names of funders and the corresponding grant IDs from the provided text"},
				{"role": "user", "content": content}
			],
			functions = [{"name": "extract_funding_info", "parameters": schema}],
			function_call = {"name": "extract_funding_info"},
			temperature = 1
		)
		entities = response.choices[0].message.function_call.arguments
		return entities
	except Exception:
		return None