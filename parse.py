from pathlib import Path

from lib.helper import load_json, group_records
from lib.character_name import load_character_name_map
from lib.character_helper import (
    get_character_by_id,
    get_released_character_list
)
from story.character_scenario import parsing_character_story
from story.character_messanger import parsing_character_messanger
from story.character_valentine import parsing_character_valentine
from story.main_story import parsing_main_story
from story.event_story import parsing_event_story

if __name__ == '__main__':
    excels_dir = Path("Excels")
    scenario_paths = [
        excels_dir / "ScenarioScriptExcelTable1.json",
        excels_dir / "ScenarioScriptExcelTable2.json",
    ]

    character_data = load_json(excels_dir / "CharacterExcelTable.json")
    scenario_data = []
    for scenario_path in scenario_paths:
        scenario_data.extend(load_json(scenario_path))
    messanger_data = load_json(excels_dir / "AcademyMessangerExcelTable.json")
    valentine_data = load_json(excels_dir / "EventContentMeetupExcelTable.json")
    scenario_mode_data = load_json(excels_dir / "ScenarioModeExcelTable.json")
    event_scenario_data = load_json(excels_dir / "EventContentScenarioExcelTable.json")
    character_name_map = load_character_name_map(excels_dir / "ScenarioCharacterNameExcelTable.json")

    character_list = get_released_character_list(character_data)
    scenario_groups = group_records(scenario_data, "GroupId")
    messanger_groups = group_records(messanger_data, "CharacterId")

    # Parsing character momotalk story from scenario & messanger
    for character_scenario in character_list:
        character_output_dir = Path("CharacterScenario", f"{character_scenario['Id']}_{character_scenario['DevName']}")
        parsing_character_story(scenario_groups, character_scenario["Id"], character_output_dir, character_name_map)
    for character_messanger in character_list:
        character_output_toml = Path("CharacterMessanger", f"{character_messanger['Id']}_{character_messanger['DevName']}.toml")
        parsing_character_messanger(messanger_groups.get(character_messanger["Id"], []), character_messanger["Id"], character_output_toml)

    # Parsing character valentine story
    for valentine_character in valentine_data:
        valentine_char_data = get_character_by_id(character_data, valentine_character["CharacterId"])
        character_valentine_toml = Path("CharacterValentine", f"{valentine_char_data['Id']}_{valentine_char_data['DevName']}.toml")
        parsing_character_valentine(
            scenario_groups.get(valentine_character["ConditionScenarioGroupId"], []),
            valentine_character["ConditionScenarioGroupId"],
            character_valentine_toml,
            character_name_map,
        )

    # Parsing main story
    parsing_main_story(scenario_mode_data, scenario_groups, Path("MainStory"), character_name_map)

    # Parsing event story
    parsing_event_story(event_scenario_data, scenario_groups, Path("EventStory"), character_name_map)
