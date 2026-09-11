from pathlib import Path
from typing import List, Dict, Any

from lib.helper import save_toml

def parsing_character_messanger(messanger_records: List[Dict[str, Any]], character_id: int, text_output_path: Path):
    if not messanger_records:
        print(f"No records found for CharacterId: {character_id}")
        return

    sorted_records = sorted(messanger_records, key=lambda r: r.get("MessageGroupId", 0))
    translations = {str(record["Id"]): record.get("MessageJP", "").strip() for record in sorted_records}

    try:
        save_toml(text_output_path, translations)
    except IOError:
        print(f"Error: Could not write output file: {text_output_path}")
