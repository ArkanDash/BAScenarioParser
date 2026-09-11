from typing import Dict, List, Any

from lib.character_name import extract_speaker, resolve_character_name

def build_translations(script_rows: List[Dict[str, Any]], group_id: int, character_name_map: dict) -> Dict[str, str]:
    translations: Dict[str, str] = {}
    for line_number, record in enumerate(script_rows, start=1):
        text_jp = record.get("TextJp") or ""
        if not text_jp.strip():
            continue
        key = f"{group_id}-{line_number}"
        speaker_kr = extract_speaker(record.get("ScriptKr"))
        if speaker_kr:
            key += f"-{resolve_character_name(character_name_map, speaker_kr)}"
        translations[key] = text_jp
    return translations
