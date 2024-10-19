import os
from abc import abstractmethod
from typing import Optional

from fastapi import Depends, HTTPException
from letta.client.client import AbstractClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from percy.metadata_store import CharacterModel
from percy.schemas.characters import CharacterGetResponse, CharacterCreateResponse, \
    CharacterDeleteResponse, CharacterUpdateResponse

# TODO(ajanitshimanga): dockerize application and spin up postgres & letta servers.

# Env variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "percy")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "percy-password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "percy-db")

# Database setup
# Update with your DB URL TODO(ajanitshimanga): Change to be db agnostic with a db provider factory.
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class AbstractPercyContext(object):
    @abstractmethod
    def create_character(self, character_id, character_name, lore, appearance, misc):
        raise NotImplementedError

    @abstractmethod
    def get_character(self, character_id: str, character_name: Optional[str] = None):
        raise NotImplementedError

    @abstractmethod
    def update_character(self, character_id: str, character_name: str, lore: str, appearance: str, misc: str):
        raise NotImplementedError

    @abstractmethod
    def delete_character(self, character_id: str):
        raise NotImplementedError

    @abstractmethod
    def list_characters(self, user_id: str):
        raise NotImplementedError


class PercyManagementContext(AbstractPercyContext):

    # TODO(ajanitshimanga): Refactor raw db to a metadata service.
    def __init__(self, db: Session, agent_client):
        self.db = db
        self.agent_client = agent_client

    def create_character(self, character_id: str, character_name, lore, appearance, misc) -> CharacterCreateResponse:
        character = CharacterModel(character_id=character_id,
                                   character_name=character_name,
                                   lore=lore,
                                   appearance=appearance,
                                   misc=misc
                                   )

        # TODO(ajanitshimanga): self.metadata_store.create_character(character) instead of coupling.

        self.db.add(character)
        self.db.commit()
        self.db.refresh(character)

        response = CharacterCreateResponse(character_id=character_id)
        return response

    def get_character(self, character_id: str, character_name: Optional[str] = None) -> CharacterGetResponse:
        # Retrieve record
        character_record = self.db.query(CharacterModel).filter(CharacterModel.id == character_id).first()

        if not character_record:
            raise HTTPException(status_code=404, detail="Character not found")

        character_id = character_record.character_id
        character_name = character_record.name
        character_description = character_record.description
        character_age = character_record.age

        return CharacterGetResponse(character_id=character_id,
                                    character_name=character_name,
                                    character_description=character_description,
                                    character_age=character_age
                                    )

    def update_character(self, character_id: str, character_name: str, lore: str, appearance: str, misc: str) -> CharacterUpdateResponse:
        # Retrieve record
        db_character = self.db.query(CharacterModel).filter(CharacterModel.id == character_id).first()

        if not db_character:
            raise HTTPException(status_code=404, detail="Character not found")

        # Set attributes only if passed
        if character_name:
            db_character.character_name = character_name

        if lore:
            db_character.lore = lore

        if appearance:
            db_character.appearance = appearance

        if misc:
            db_character.misc = misc

        self.db.commit()
        self.db.refresh(db_character)   # We don't use the record after so isn't important.

        return CharacterUpdateResponse(character_id)

    def delete_character(self, character_id: str) -> CharacterDeleteResponse:
        # TODO(ajanitshimanga): hide guts / direct db access to a DataAccess class rather than in server endpoints.
        db_character = self.db.query(CharacterModel).filter(CharacterModel.id == character_id).first()
        if not db_character:
            raise HTTPException(status_code=404, detail="Character not found")

        self.db.delete(db_character)
        self.db.commit()

        CharacterDeleteResponse(character_id=character_id, character_name=str(character_name))
        return

    def list_characters(self):
        # TODO: Default path
        raise NotImplementedError


# Database dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Letta dependency for agents
def get_letta_client():
    from letta import create_client

    letta_client = create_client()
    return letta_client


# Service instance using the stubbed database
def get_percy_server(db: Session = Depends(get_db),
                     letta_client: AbstractClient = Depends(get_letta_client())) -> PercyManagementContext:
    return PercyManagementContext(db, letta_client)
