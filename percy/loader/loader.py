import json
import os
from pathlib import Path

from abc import ABC, abstractmethod

from pydantic import BaseModel
from typing import List, Optional

from percy.utils import RESOURCE_PATH, PERCY_PROJECT_ROOT, RELATIVE_RESOURCE_PATH

ability_types = ["BASIC", "SIGNATURE", "ULTIMATE"]


class Ability(BaseModel):
    type: str  # Basic, Signature, Ultimate
    name: str
    description: str


class Relationship(BaseModel):
    name: str
    description: str


class Character(BaseModel):
    character_name: str
    details: dict  # define a more specific model for details if needed
    past: str
    appearance: str
    relationships: List[Relationship]
    abilities: List[Ability]
    weaknesses: List[str]
    strengths: List[str]
    affiliations: List[str]
    phrases: Optional[List[str]] = []  # Optional empty list
    interests: Optional[List[str]] = []  # Optional empty list


class CharacterRepository(ABC):
    @abstractmethod
    def load(self) -> Character:
        raise NotImplementedError

    @abstractmethod
    def save(self, character: Character):
        raise NotImplementedError


class JsonCharacterRepository(CharacterRepository):
    def __init__(self, filename: str):
        # Define project root and resource path

        if not filename.startswith(RELATIVE_RESOURCE_PATH):
            raise ValueError(f"Relative resource path must be specified. Got: {RESOURCE_PATH}")

        self.filename = os.path.join(PERCY_PROJECT_ROOT, filename)

    def load(self) -> dict:
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"{self.filename} does not exist.")
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return data #Character(**data)  # Unpack the dictionary into the Character model

    def save(self, character_dict: dict):
        with open(self.filename, 'w') as file:
            json.dump(character_dict, file, indent=4)  # Use .dict() for serialization
