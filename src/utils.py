import os
import uuid
import json
from pathlib import Path

def set_multiline_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        delimiter = uuid.uuid1()
        print(f'{name}<<{delimiter}', file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)

def set_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{name}={value}', file=fh)

def load_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)
    
def read_file(file_path: str):
    with open(file_path, 'r') as file:
        return file.read()

def get_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key is None:
        raise EnvironmentError("GEMINI_API_KEY is not set.")
    return api_key
