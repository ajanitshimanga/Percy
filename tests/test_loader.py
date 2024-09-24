from percy.loader.loader import JsonCharacterRepository


def test_json_loader():

    # Specify the relative path to your JSON file
    relative_file_path = "resources/characters/valorant/agents/brimstone.json"

    # Create repository
    json_repository = JsonCharacterRepository(relative_file_path)

    # Load from both

    json_entity = json_repository.load()

    assert json_entity["character_name"] == "brimstone"

    # Modify entity
    json_entity["character_name"] = "brimstone-evil-modified"

    # Save entity
    json_repository.save(json_entity)

    # Load new
    json_entity = json_repository.load()

    assert json_entity["character_name"] == "brimstone-evil-modified"
