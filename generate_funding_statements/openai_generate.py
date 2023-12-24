import os
from openai import OpenAI

client = OpenAI(
	api_key=os.environ['OPENAI_API_KEY']
)

def openai_generate(prompt, funding_statement):
	content = f'{prompt} {funding_statement} | Ouput: '
	try:
		response = client.chat.completions.create(
			# In testing, current version of gpt-3.5-turbo was 
			# unable to preserve bracketed text, so defaulting
			# to legacy model with better performance on this task.
			model="gpt-3.5-turbo-0301",
			messages=[
				{"role": "user", "content": content}
			],
			temperature=1
		)
		entities = response.choices[0].message.content
		return entities
	except Exception:
		return None
