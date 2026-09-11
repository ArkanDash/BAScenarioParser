import json

from collections import defaultdict
from pathlib import Path
from typing import Union

def load_json(json_path: Union[str, Path]):
    try:
        with open(json_path, "r", encoding="utf-8") as infile:
            raw_data = json.load(infile)
        if isinstance(raw_data, dict) and "DataList" in raw_data:
            raw_data = raw_data["DataList"]
        return raw_data
    except FileNotFoundError as e:
        print(f"Error: Input JSON file not found at {json_path}")
        raise e
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from {json_path}")
        raise e

def group_records(records, key: str) -> dict:
    grouped = defaultdict(list)
    for record in records:
        value = record.get(key)
        if value is not None:
            grouped[value].append(record)
    return dict(grouped)

def save_toml(toml_path: Path, translations: dict):
    lines = ["[translation]"]
    for key, value in translations.items():
        lines.append(f"{json.dumps(str(key), ensure_ascii=False)} = {json.dumps(str(value), ensure_ascii=False)}")
    toml_path.parent.mkdir(parents=True, exist_ok=True)
    toml_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")