import uuid

from pydantic import BaseModel, Field
from typing import List, Optional


# Pydantic models for request/response
# NOTe: Cut model bloat for now, increase when needed. Keeping light
class CharacterCreateRequest(BaseModel):
    character_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    lore: Optional[str] = None
    appearance: Optional[str] = None
    misc: Optional[str] = None


class CharacterCreateResponse(BaseModel):
    character_id: Optional[str] = None


class CharacterGetRequest(BaseModel):
    character_id: str
    character_name: str


class CharacterGetResponse(BaseModel):
    character_id: str
    lore: Optional[str] = None
    appearance: Optional[str] = None
    misc: Optional[List[str]] = None


class CharacterUpdateRequest(BaseModel):
    character_id: str
    character_name: Optional[str] = None
    lore: Optional[str] = None
    appearance: Optional[str] = None
    misc: Optional[List[str]] = None


class CharacterUpdateResponse(BaseModel):
    character_id: str


class CharacterDeleteRequest(BaseModel):
    character_id: str


class CharacterDeleteResponse(BaseModel):
    character_id: str
    character_name: str
