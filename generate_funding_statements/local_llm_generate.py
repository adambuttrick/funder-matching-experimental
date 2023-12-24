import os
import json
import requests

def local_llm_generate(prompt, funding_statement):
	content = f'{prompt} {funding_statement} | Ouput: '
	data = {
	"model": "openchat",
	"prompt": content,
	"stream": False
	}
	r = requests.post('http://localhost:11434/api/generate', json=data)
	response = r.json()
	return response['response']