import uuid

import pytest

from percy.client.client import LocalClientPercy
from percy.schemas.characters import CharacterCreateRequest
from percy.server.server import SessionLocal, get_letta_client, PercyManagementContext


test_character_json = {"name": "brimstone",
                       "lore": "Coming from the USA, Brimstone is a tech user and veteran soldier that has seen all kinds of battles, never leaving a wounded companion behind. He was the first to join the VALORANT PROTOCOL alongside Viper, and is currently its leader. Brimstone has a very stubborn personality, acting as a 'father figure' for the group. Named the 'Old Dog' due to his age, he is treated as a leader and titled 'Commander' and 'Captain' by the other Agents. He is in charge, in some part, of picking and hiring new Agents to VP. Unlike Viper, Brimstone has a positive attitude regarding the youth in the team and hiring new members. Alongside a bottle of scotch and an incendiary grenade, Brimstone uses technology to dominate the battlefield. He has access to an array of satellite-based abilities that allow him to deploy large smoke clouds and launch orbital laser attacks through a bracer on his left arm. His bracer was designed by Killjoy. Brimstone's status as the eldest member of the PROTOCOL makes him a common target for jokes about his age, but most of them are turned down because of his sheer skill. He also seems to face considerable difficulty with handling technology and devices, oftentimes getting locked out of his bracer simply because he forgot the password. Interestingly, because his age is likely around 45-50, and the year in which the game takes place is around 2050 (this year has been retconned and the year Valorant takes place in is unknown), Brimstone is likely a millennial or younger, born at the latest in the late 90s. This would mean that he probably grew up with devices and the internet, which generates some confusion as to the cause of his difficulty with technology. Brimstone does have his own office, located under the Range. It contains several images (some of which include a childhood friend posing with him). The office also contains his phone and laptop, which can be interacted with to reveal a voicemail or email sent to him by one of the Agents. These messages are periodically updated every patch. For an archive of these, along with a more detailed description of his office, see its page.",
                       "appearance": "Brimstone wears an orange army beret with a patch that depicts two 'V' symbols, one inside the other. He wears Military Attire that is likely the standardized K-SEC Uniform. His metal breastplate is stamped with the number 01, referring to him being the first Agent to join the PROTOCOL. The left strap for the armor features a plate with the Kingdom Logo, which is also present on his right hand's glove. His left shoulder plate is stamped with the VALORANT PROTOCOL logo. The backplate of his armor allows for his Stim Beacon to attach in an easy-to-reach position. On his left hand is his Bracer, a metal device which displays an orange screen, used to control his Sky Smokes and Orbital Strike. When activated, the screen generates an orange holographic map. In the WARM UP cinematic, we see Brimstone with his rolled-up sleeves looser than normal, allowing us a view of a tattoo he has on his upper right arm. The pattern of the tattoo is similar to that of the Peacekeeper Sheriff, which is obtainable in-game by completing Brimstone's contract.",
                       "misc": "misc input i am on top of the world! :))"
                       }


@pytest.fixture(scope="function")
def percy():

    # before
    session = SessionLocal()

    yield LocalClientPercy()

    # after - clean up and close
    session.rollback()
    session.close()


def test_characters_crud(percy):
    # Percy server instance.
    percy_server = percy

    # Test character setup
    test_character_name = test_character_json["name"]
    test_character_lore = test_character_json["lore"]
    test_character_appearance = test_character_json["appearance"]
    test_character_misc = test_character_json["misc"]

    create_character_request = CharacterCreateRequest(character_name=test_character_name,
                                                      lore=test_character_lore,
                                                      appearance=test_character_appearance,
                                                      misc=test_character_misc)

    # Create character path - need to rewrite to separate table for testing.
    create_character_response = percy_server.create_character(create_character_request)

    assert create_character_response.character_id is not None
    assert type(create_character_response.character_id) == str
