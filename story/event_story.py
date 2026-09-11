from pathlib import Path
from typing import Dict

from lib.helper import save_toml
from lib.scenario import build_translations

def parsing_event_story(event_data, scenario_groups: Dict[int, list], output_root: Path, character_name_map: dict):
    written_files = 0
    written_lines = 0

    for event_record in event_data:
        event_content_id = event_record.get("EventContentId")
        order = event_record.get("Order")
        for group_id in event_record.get("ScenarioGroupId") or []:
            script_rows = scenario_groups.get(group_id)
            if not script_rows:
                continue

            translations = build_translations(script_rows, group_id, character_name_map)
            if not translations:
                continue

            output_file = Path(output_root, str(event_content_id), f"{group_id}_{order}.toml")
            save_toml(output_file, translations)
            written_files += 1
            written_lines += len(translations)

    print(f"Event story: wrote {written_files} files, {written_lines} lines.")
