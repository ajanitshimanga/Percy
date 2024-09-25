import uuid

from pydantic import BaseModel
from typing import List, Optional, Dict


# Pydantic models for request/response
class CharacterCreateRequest(BaseModel):
    character_name: str
    lore: Optional[str] = None
    past: Optional[str] = None
    appearance: Optional[str] = None
    relationships: Optional[Dict] = None  # Assuming relationships are stored as a dictionary
    abilities: Optional[Dict] = None  # Assuming abilities are stored as a dictionary

    weakness: Optional[str] = None
    strengths: Optional[str] = None
    affiliations: Optional[str] = None
    phrases: Optional[List[str]] = None
    interests: Optional[List[str]] = None


class CharacterCreateResponse(BaseModel):
    character_id: uuid.UUID


class CharacterGetRequest(BaseModel):
    character_id: uuid.UUID


class CharacterGetResponse(BaseModel):
    character_id: uuid.UUID
    character_dict: dict


class CharacterUpdateRequest(BaseModel):
    character_id: str
    character_name: str
    lore: Optional[str] = None
    past: Optional[str] = None
    appearance: Optional[str] = None
    relationships: Optional[Dict] = None  # Assuming relationships are stored as a dictionary
    abilities: Optional[Dict] = None  # Assuming abilities are stored as a dictionary

    weakness: Optional[str] = None
    strengths: Optional[str] = None
    affiliations: Optional[str] = None
    phrases: Optional[List[str]] = None
    interests: Optional[List[str]] = None


class CharacterUpdateResponse(BaseModel):
    character_id: str


class CharacterDeleteRequest(BaseModel):
    character_id: uuid.UUID


class CharacterDeleteResponse(BaseModel):
    character_id: uuid.UUID
    character_name: str
