import uuid

from pydantic import BaseModel
from typing import List, Optional, Dict

from sqlalchemy.dialects.postgresql import UUID


# Pydantic models for request/response
class CharacterCreateRequest(BaseModel):
    user_id: UUID
    character_name: str
    lore: Optional[str] = None
    past: Optional[str] = None
    appearance: Optional[str] = None
    abilities: Optional[Dict] = None  # Assuming abilities are stored as a dictionary

    weakness: Optional[str] = None
    strengths: Optional[str] = None
    affiliations: Optional[str] = None
    phrases: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    relationships: Optional[Dict] = None  # Assuming relationships are stored as a dictionary


class CharacterCreateResponse(BaseModel):
    character_id: uuid.UUID
