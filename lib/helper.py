import os
import json

def load_json(json_path: str):
    try:
        with open(json_path, "r", encoding="utf-8") as infile:
            raw_data = json.load(infile)
        return raw_data
    except FileNotFoundError as e:
        print(f"Error: Input JSON file not found at {json_path}")
        raise e
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from {json_path}")
        raise e

def save_json(json_path: str, data: dict):
    try:
        directory = os.path.dirname(json_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(json_path, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: Could not save JSON to {json_path}")
        raise e