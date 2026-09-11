from pathlib import Path
from collections import defaultdict
from typing import Dict

from lib.helper import save_toml
from lib.scenario import build_translations

def parsing_character_story(scenario_groups: Dict[int, list], character_id: int, text_output_dir: Path, character_name_map: dict):
    grouped_translations: Dict[int, Dict[str, str]] = defaultdict(dict)

    first_char_group = int(f"{character_id}00")
    last_char_group = int(f"{character_id}99")

    for group_id, records in scenario_groups.items():
        if not (first_char_group <= group_id <= last_char_group):
            continue
        translations = build_translations(records, group_id, character_name_map)
        if translations:
            grouped_translations[group_id] = translations

    if not grouped_translations:
        print("No valid entries found in the GroupId range.")
        return

    text_output_dir.mkdir(parents=True, exist_ok=True)

    total_lines = 0
    for group_id, translations in grouped_translations.items():
        output_file = text_output_dir / f"{character_id}_{group_id}.toml"
        try:
            save_toml(output_file, translations)
            total_lines += len(translations)
        except IOError:
            print(f"Error: Could not write file for GroupId {group_id}: {output_file}")
