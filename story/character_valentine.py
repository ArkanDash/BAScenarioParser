from pathlib import Path
from typing import Dict, List, Any

from lib.helper import save_toml
from lib.scenario import build_translations

def parsing_character_valentine(script_rows: List[Dict[str, Any]], scenario_id: int, output_path: Path, character_name_map: dict) -> None:
    translations: Dict[str, str] = build_translations(script_rows, scenario_id, character_name_map)

    if not translations:
        print("No valid entries found in the GroupId range.")
        return

    try:
        save_toml(output_path, translations)
    except IOError:
        print(f"Error: Could not write file for GroupId {scenario_id}: {output_path}")
