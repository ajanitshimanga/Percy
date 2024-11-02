from abc import ABC, abstractmethod
from typing import List

import requests
from percy.schemas.characters import CharacterCreateResponse, CharacterCreateRequest, \
    CharacterGetResponse, CharacterUpdateRequest, CharacterUpdateResponse, CharacterDeleteResponse


class Client(ABC):

    @abstractmethod
    def create_character(self, request: CharacterCreateRequest) -> CharacterCreateResponse:
        raise NotImplementedError

    @abstractmethod
    def get_character(self, character_id: str) -> CharacterGetResponse:
        raise NotImplementedError

    @abstractmethod
    def update_character(self, request: CharacterUpdateRequest) -> CharacterUpdateResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_character(self, character_id: str) -> CharacterDeleteResponse:
        raise NotImplementedError

    @abstractmethod
    def list_characters(self) -> List[CharacterGetResponse]:
        raise NotImplementedError


class RestClientPercy(Client):

    def __init__(self, base_uri: str = "", token: str = "dummy_token"):
        self.base_uri = base_uri
        self.token = token
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {token}"
        }

    def create_character(self, request: CharacterCreateRequest) -> CharacterCreateResponse:
        response = requests.post(f"{self.base_uri}/characters", headers=self.headers, json=request.model_dump())
        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to create character: {response.text}")
        return CharacterCreateResponse(**response.json())

    def get_character(self, character_id: str) -> CharacterGetResponse:
        response = requests.get(f"{self.base_uri}/characters/{character_id}", headers=self.headers)
        print(response)
        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to get character: {response.text}")
        return CharacterGetResponse(**response.json())

    def update_character(self, request: CharacterUpdateRequest) -> CharacterUpdateResponse:
        response = requests.patch(f"{self.base_uri}/characters/{request.character_id}",
                                  headers=self.headers,
                                  json=request.model_dump())
        print(response)

        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to update character: {response.text}")
        return CharacterUpdateResponse(**response.json())

    def delete_character(self, character_id: str) -> CharacterDeleteResponse:
        response = requests.delete(f"{self.base_uri}/characters/{character_id}", headers=self.headers)
        print(response)

        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to delete character: {response.text}")
        return CharacterDeleteResponse(**response.json())

    def list_characters(self) -> List[CharacterGetResponse]:
        response = requests.get(f"{self.base_uri}/characters", headers=self.headers)
        print(response)

        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to list characters: {response.text}")
        return [CharacterGetResponse(**character) for character in response.json()]


class LocalClientPercy(Client):

    def __init__(self):
        from percy.server.server import get_local_percy_server
        self._server = get_local_percy_server()

    def create_character(self, request: CharacterCreateRequest) -> CharacterCreateResponse:
        with self._server as percy:
            response = percy.create_character(**request.dict())
        return CharacterCreateResponse(**response.dict())

    def get_character(self, character_id: str) -> CharacterGetResponse:
        with self._server as percy:
            response = percy.get_character(character_id)
        return CharacterGetResponse(**response.dict())

    def update_character(self, request: CharacterUpdateRequest) -> CharacterUpdateResponse:
        with self._server as percy:
            response = percy.update_character(**request.dict())
        return CharacterUpdateResponse(**response.dict())

    def delete_character(self, character_id: str) -> CharacterDeleteResponse:
        with self._server as percy:
            response = percy.delete_character(character_id)
        return CharacterDeleteResponse(**response.dict())

    def list_characters(self) -> List[CharacterGetResponse]:
        # TODO(ajanitshimanga): implementation

        char_id = "implement"
        characters = self._server.list_characters(char_id)  # Assuming this returns a list of character dicts
        return [CharacterGetResponse(**character) for character in characters]

    def send_message(self, character_id: str, message: str):
        with self._server as percy:
            response = percy.send_message(character_id=character_id, message=message)
        return response


if __name__ == "__main__":
    local_client = LocalClientPercy()

    test_character_json = {"name": "brimstone",
                           "lore": "Coming from the USA, Brimstone is a tech user and veteran soldier that has seen all kinds of battles, never leaving a wounded companion behind. He was the first to join the VALORANT PROTOCOL alongside Viper, and is currently its leader. Brimstone has a very stubborn personality, acting as a 'father figure' for the group. Named the 'Old Dog' due to his age, he is treated as a leader and titled 'Commander' and 'Captain' by the other Agents. He is in charge, in some part, of picking and hiring new Agents to VP. Unlike Viper, Brimstone has a positive attitude regarding the youth in the team and hiring new members. Alongside a bottle of scotch and an incendiary grenade, Brimstone uses technology to dominate the battlefield. He has access to an array of satellite-based abilities that allow him to deploy large smoke clouds and launch orbital laser attacks through a bracer on his left arm. His bracer was designed by Killjoy. Brimstone's status as the eldest member of the PROTOCOL makes him a common target for jokes about his age, but most of them are turned down because of his sheer skill. He also seems to face considerable difficulty with handling technology and devices, oftentimes getting locked out of his bracer simply because he forgot the password. Interestingly, because his age is likely around 45-50, and the year in which the game takes place is around 2050 (this year has been retconned and the year Valorant takes place in is unknown), Brimstone is likely a millennial or younger, born at the latest in the late 90s. This would mean that he probably grew up with devices and the internet, which generates some confusion as to the cause of his difficulty with technology. Brimstone does have his own office, located under the Range. It contains several images (some of which include a childhood friend posing with him). The office also contains his phone and laptop, which can be interacted with to reveal a voicemail or email sent to him by one of the Agents. These messages are periodically updated every patch. For an archive of these, along with a more detailed description of his office, see its page.",
                           "appearance": "Brimstone wears an orange army beret with a patch that depicts two 'V' symbols, one inside the other. He wears Military Attire that is likely the standardized K-SEC Uniform. His metal breastplate is stamped with the number 01, referring to him being the first Agent to join the PROTOCOL. The left strap for the armor features a plate with the Kingdom Logo, which is also present on his right hand's glove. His left shoulder plate is stamped with the VALORANT PROTOCOL logo. The backplate of his armor allows for his Stim Beacon to attach in an easy-to-reach position. On his left hand is his Bracer, a metal device which displays an orange screen, used to control his Sky Smokes and Orbital Strike. When activated, the screen generates an orange holographic map. In the WARM UP cinematic, we see Brimstone with his rolled-up sleeves looser than normal, allowing us a view of a tattoo he has on his upper right arm. The pattern of the tattoo is similar to that of the Peacekeeper Sheriff, which is obtainable in-game by completing Brimstone's contract.",
                           "misc": "misc input i am on top of the world! :))"
                           }

    # # Verify - Create route
    # test_character_name = test_character_json["name"]
    # test_character_lore = test_character_json["lore"]
    # test_character_appearance = test_character_json["appearance"]
    # test_character_misc = test_character_json["misc"]
    #
    # create_character_request = CharacterCreateRequest(character_name=test_character_name,
    #                                                   lore=test_character_lore,
    #                                                   appearance=test_character_appearance,
    #                                                   misc=test_character_misc)
    #
    # create_character_response = local_client.create_character(create_character_request)
    # print("THIS IS THE RESPONSE I GOT:", create_character_response)

    char_id = '94f71df9-2712-4e23-80f7-2e6f62c601d3'

    message = "Can you generate me some simple and concise ideas to show their conflicts?"

    response = local_client.send_message(char_id, message)

    print("THIS IS THE RESPONSE I GOT:", response.messages[0].internal_monologue)

    # # Verify - get path
    # character_id_for_brimstone = '375451b8-da6b-4db9-a1ba-efb4b9c16d81'
    #
    # get_response = local_client.get_character(character_id_for_brimstone)
    #
    # print("THIS IS A GET RESPONSE: ")
    # for key in get_response.dict().keys():
    #     print(key + "  ----   ", get_response.dict()[key])
    #     print("\n\n\n")



# from abc import ABC, abstractmethod
# from typing import List
#
# import requests
#
# from percy.schemas.characters import CharacterCreateResponse, CharacterCreateRequest, CharacterGetResponse, \
#     CharacterUpdateRequest, CharacterUpdateResponse, CharacterDeleteRequest, CharacterDeleteResponse
#
#
# class Client(ABC):
#
#     @abstractmethod
#     def create_character(self, character_name: str, character_dict: dict):
#         raise NotImplementedError
#
#     @abstractmethod
#     def get_character(self, character_id: str):
#         raise NotImplementedError
#
#     @abstractmethod
#     def update_character(self, character_id: str, character_name: str, character_dict: dict):
#         raise NotImplementedError
#
#     @abstractmethod
#     def delete_character(self, character_id: str):
#         raise NotImplementedError
#
#     @abstractmethod
#     def list_characters(self):
#         raise NotImplementedError
#
#
# class RestClient(Client):
#     """
#     client allows standard-level operations on the Percy server.
#     - Creating characters
#     - Getting characters
#     - Deleting characters
#     - Updating characters
#     - Listing characters
#
#     """
#
#     def __init__(self, base_uri: str="", token: str="dummy_token"):
#         self.base_uri = base_uri
#         self.token = token
#         self.headers = {"accept": "application/json", "content-type": "application/json",
#                         "authorization": f"Bearer {token}"}
#
#     def create_character(self, character_name: str, character_dict: dict) -> CharacterCreateResponse:
#
#         # Validate request
#         request = CharacterCreateRequest(
#             character_name=character_name,  # Only required field!
#             lore=character_dict.get("lore", None),
#             past=character_dict.get("past", None),
#             appearance=character_dict.get("appearance", None),
#             relationships=character_dict.get("relationships", None),
#             abilities=character_dict.get("abilities", None),
#             weakness=character_dict.get("weakness", None),
#             strengths=character_dict.get("strengths", None),
#             affiliations=character_dict.get("affiliations", None),
#             phrases=character_dict.get("phrases", None),
#             interests=character_dict.get("interests", None),
#         )
#
#         response = requests.post(f"{self.base_uri}/characters", headers=self.headers, json=request.model_dump())
#         if response.status_code != 200:
#             raise ValueError(f"Status {response.status_code} - Failed to create character: {response.text}")
#
#         return CharacterCreateResponse(**response.json())
#
#     def get_character(self, character_id: str) -> CharacterGetResponse:
#         response = requests.get(f"{self.base_uri}/characters/{character_id}", headers=self.headers)
#
#         if response.status_code != 200:
#             raise ValueError(f"Status {response.status_code} - Failed to get character: {response.text}")
#
#         return CharacterGetResponse(**response.json())
#
#     def update_character(self, character_id: str, character_name: str, character_dict: dict) -> CharacterUpdateResponse:
#
#         # Validate request
#         request = CharacterUpdateRequest(
#             character_id=character_id,
#             character_name=character_name,
#             lore=character_dict.get("lore", None),
#             past=character_dict.get("past", None),
#             appearance=character_dict.get("appearance", None),
#             relationships=character_dict.get("relationships", None),
#             abilities=character_dict.get("abilities", None),
#             weakness=character_dict.get("weakness", None),
#             strengths=character_dict.get("strengths", None),
#             affiliations=character_dict.get("affiliations", None),
#             phrases=character_dict.get("phrases", None),
#             interests=character_dict.get("interests", None),
#         )
#
#         response = requests.patch(f"{self.base_uri}/characters/{character_id}",
#                                   headers=self.headers,
#                                   json=request.model_dump())
#
#         if response.status_code != 200:
#             raise ValueError(f"Status {response.status_code} - Failed to update character: {response.text}")
#
#         return CharacterUpdateResponse(**response.json())
#
#     def delete_character(self, character_id: str) -> CharacterDeleteResponse:
#
#         # Validate request
#         request = CharacterDeleteRequest(
#             character_id=character_id
#         )
#
#         response = requests.delete(f"{self.base_uri}/characters/{request.character_id}",
#                                    headers=self.headers)
#
#         if response.status_code != 200:
#             raise ValueError(f"Status {response.status_code} - Failed to delete character: {response.text}")
#
#         return CharacterDeleteResponse(**response.json())
#
#     def list_characters(self) -> List[CharacterGetResponse]:
#         response = requests.get(f"{self.base_uri}/characters", headers=self.headers)
#
#         if response.status_code != 200:
#             raise ValueError(f"Status {response.status_code} - Failed to list character: {response.text}")
#
#         return [CharacterGetResponse(**character) for character in response.json()]
#
#
# class LocalClient(Client):
#
#     def __init__(self):
#         from percy.server.server import PercyManagementContext
#         self.server = PercyManagementContext()
#
#     @abstractmethod
#     def create_character(self, character_name: str, character_dict: dict):
#         raise NotImplementedError
#
#     @abstractmethod
#     def get_character(self, character_id: str):
#         raise NotImplementedError
#
#     @abstractmethod
#     def update_character(self, character_id: str, character_name: str, character_dict: dict):
#         raise NotImplementedError
#
#     @abstractmethod
#     def delete_character(self, character_id: str):
#         raise NotImplementedError
#
#     @abstractmethod
#     def list_characters(self):
#         raise NotImplementedError
