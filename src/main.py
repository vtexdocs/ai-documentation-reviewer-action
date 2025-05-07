from google import genai
import sys
import os
import json
from utils import get_api_key, load_json_file
from categorize_doc import categorize_doc
from generate_feedback import generate_feedback

RULES_MAPPING = load_json_file('/action/config/rules_mapping.json')

def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    file_path = os.getenv('FILE_PATHS')
    doc_metadata = categorize_doc(file_path, client)
    print(doc_metadata)
    
    doc_type = doc_metadata["type"]
    if doc_type not in RULES_MAPPING:
        print(f"No rules found for documentation type: {doc_type}")
        sys.exit(1)
    
    rules_path = RULES_MAPPING[doc_type]
    doc_rules = load_json_file(rules_path)
        
    generate_feedback(file_path, doc_metadata, doc_rules, client)

if __name__ == "__main__":
    main()
