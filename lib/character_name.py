import xxhash

from lib.helper import load_json

def load_character_name_map(json_path):
    rows = load_json(json_path)
    return {row["CharacterName"]: row.get("NameJP", "") for row in rows}

def extract_speaker(script_kr):
    if not script_kr:
        return None

    speaker = None
    for script_line in str(script_kr).split("\n"):
        line_speaker = _extract_line_speaker(script_line)
        if line_speaker:
            speaker = line_speaker
    return speaker

def _extract_line_speaker(script_line):
    parts = script_line.split(";")
    command = parts[0].strip().lower()

    if command == "#na" or command == "#q":
        if len(parts) == 3:
            return parts[1].strip()
        return None

    if command.startswith("#"):
        return None

    if len(parts) < 2 or (len(parts) == 2 and not parts[1]):
        return None

    return parts[1].strip()

def resolve_character_name(character_name_map: dict, kr_name):
    if not kr_name:
        return None
    hash_key = xxhash.xxh32(str(kr_name).encode("utf-8")).intdigest()
    jp_name = character_name_map.get(hash_key)
    return jp_name if jp_name else kr_name
