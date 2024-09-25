from abc import ABC, abstractmethod
from typing import List

import requests

from percy.client.model.characters import CharacterCreateResponse, CharacterCreateRequest, CharacterGetResponse, \
    CharacterUpdateRequest, CharacterUpdateResponse, CharacterDeleteRequest, CharacterDeleteResponse


class Client(ABC):

    @abstractmethod
    def create_character(self, character_name: str, character_dict: dict):
        raise NotImplementedError

    @abstractmethod
    def get_character(self, character_id: str):
        raise NotImplementedError

    @abstractmethod
    def update_character(self, character_id: str, character_name: str, character_dict: dict):
        raise NotImplementedError

    @abstractmethod
    def delete_character(self, character_id: str):
        raise NotImplementedError

    @abstractmethod
    def list_characters(self):
        raise NotImplementedError


class RestClient(Client):
    """
    client allows standard-level operations on the Percy server.
    - Creating characters
    - Getting characters
    - Deleting characters
    - Updating characters
    - Listing characters

    """

    def __init__(self, base_uri: str, token: str):
        self.base_uri = base_uri
        self.token = token
        self.headers = {"accept": "application/json", "content-type": "application/json",
                        "authorization": f"Bearer {token}"}

    def create_character(self, character_name: str, character_dict: dict) -> CharacterCreateResponse:

        # Validate request
        request = CharacterCreateRequest(
            character_name=character_name,  # Only required field!
            lore=character_dict.get("lore", None),
            past=character_dict.get("past", None),
            appearance=character_dict.get("appearance", None),
            relationships=character_dict.get("relationships", None),
            abilities=character_dict.get("abilities", None),
            weakness=character_dict.get("weakness", None),
            strengths=character_dict.get("strengths", None),
            affiliations=character_dict.get("affiliations", None),
            phrases=character_dict.get("phrases", None),
            interests=character_dict.get("interests", None),
        )

        response = requests.post(f"{self.base_uri}/characters", headers=self.headers, json=request.model_dump())
        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to create character: {response.text}")

        return CharacterCreateResponse(**response.json())

    def get_character(self, character_id: str) -> CharacterGetResponse:
        response = requests.get(f"{self.base_uri}/characters/{character_id}", headers=self.headers)

        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to get character: {response.text}")

        return CharacterGetResponse(**response.json())

    def update_character(self, character_id: str, character_name: str, character_dict: dict) -> CharacterUpdateResponse:

        # Validate request
        request = CharacterUpdateRequest(
            character_id=character_id,
            character_name=character_name,
            lore=character_dict.get("lore", None),
            past=character_dict.get("past", None),
            appearance=character_dict.get("appearance", None),
            relationships=character_dict.get("relationships", None),
            abilities=character_dict.get("abilities", None),
            weakness=character_dict.get("weakness", None),
            strengths=character_dict.get("strengths", None),
            affiliations=character_dict.get("affiliations", None),
            phrases=character_dict.get("phrases", None),
            interests=character_dict.get("interests", None),
        )

        response = requests.patch(f"{self.base_uri}/characters/{character_id}",
                                  headers=self.headers,
                                  json=request.model_dump())

        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to update character: {response.text}")

        return CharacterUpdateResponse(**response.json())

    def delete_character(self, character_id: str) -> CharacterDeleteResponse:

        # Validate request
        request = CharacterDeleteRequest(
            character_id=character_id
        )

        response = requests.delete(f"{self.base_uri}/characters/{request.character_id}",
                                   headers=self.headers)

        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to delete character: {response.text}")

        return CharacterDeleteResponse(**response.json())

    def list_characters(self) -> List[CharacterGetResponse]:
        response = requests.get(f"{self.base_uri}/characters", headers=self.headers)

        if response.status_code != 200:
            raise ValueError(f"Status {response.status_code} - Failed to list character: {response.text}")

        return [CharacterGetResponse(**character) for character in response.json()]
