from percy.loader.loader import JsonCharacterRepository


def test_json_loader():
    # TODO(ajanitshimanga): Clean up messy adhoc setup.

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
    json_repository.save(json_entity)  # TODO: Save path should be modified with a location so it doesn't auto overwrite

    # Load new
    json_entity = json_repository.load()

    assert json_entity["character_name"] == "brimstone-evil-modified"

    json_entity["character_name"] == "brimstone"
    json_repository.save(json_entity)
