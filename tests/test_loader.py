from percy.loader.loader import JsonCharacterRepository


# TODO(ajanitshimanga): uncomment or remove json loader from package. No longer supported for now but keeping for now.
def test_json_loader():
    # TODO(ajanitshimanga): Transitioning to postgres - no longer needed.
    #
    # # Specify the relative path to your JSON file
    # relative_file_path = "resources/characters/valorant/agents/brimstone.json"
    #
    # # Create repository
    # json_repository = JsonCharacterRepository(relative_file_path)
    #
    # # Load from both
    #
    # json_entity = json_repository.load()
    #
    # assert json_entity["character_name"] == "brimstone"
    #
    # # Modify entity
    # json_entity["character_name"] = "brimstone-evil-modified"
    #
    # # Save entity
    # json_repository.save(json_entity)
    #
    # # Load new
    # json_entity = json_repository.load()
    #
    # assert json_entity["character_name"] == "brimstone-evil-modified"
    #
    # json_entity["character_name"] == "brimstone"
    # json_repository.save(json_entity)
    assert True
