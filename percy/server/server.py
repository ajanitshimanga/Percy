import os
from abc import abstractmethod
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from letta.client.client import AbstractClient
from letta.schemas.memory import ChatMemory
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from percy.metadata_store import CharacterModel, DataStore, Base
from percy.schemas.characters import CharacterGetResponse, CharacterCreateResponse, \
    CharacterDeleteResponse, CharacterUpdateResponse

# Load environment variables from .env file
load_dotenv()

# Env variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "percy")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "percy-password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "percy-db")
db_port = str(5432)

# Database setup
# Update with your DB URL TODO(ajanitshimanga): Change to be db agnostic with a db provider factory.
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5433/{POSTGRES_DB}"
#DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgresql-store:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine) # create tables

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class AbstractPercyContext(object):
    @abstractmethod
    def create_character(self, character_id, character_name, lore, appearance, misc):
        raise NotImplementedError

    @abstractmethod
    def get_character(self, character_id: str, character_name: Optional[str] = None) -> CharacterGetResponse:
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

    @abstractmethod
    def send_message(self, character_id: str, message: str, character_name: Optional[str] = None):
        raise NotImplementedError


class PercyManagementContext(AbstractPercyContext):

    # TODO(ajanitshimanga): Refactor raw db session to a metadata service.
    def __init__(self, db_session: Optional[Session] = None,  agent_client: Optional[AbstractClient] = None, datastore: DataStore = None):
        self.db_session = db_session or SessionLocal()
        self.agent_client = agent_client or get_letta_client()
        self.datastore = datastore   # TODO: plumb in data store to phase out db_session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close db after use
        self.db_session.close()

    # TODO(ajanitshimanga): self.metadata_store.create_character(character) instead of coupling.
    def create_character(self, character_id: str, character_name: str, lore: str, appearance: str, misc: str) -> CharacterCreateResponse:

        # Create a chat memory block for agent
        # TODO(ajanitshimang): implementation choice to make, either increase memory block size to larger or make lore,
        #  appearace, and misc input into the archival memory so it uses RAG like instead to load into memory.
        user_name = "Eren-Default"
        base_persona = f"""
        I am {character_name} and I must answer user questions, scenarios, and hypothetical interactions with other entities
        that is consistent with my persona information and all data sources that I have access and knowledge of. My goal is to be as detailed as possible in answering character related writing questions with the user.

        These are the relevant data related to my self and persona:
        
        Name: {character_name}
        
        Lore: {lore}
        
        appearance: {appearance}
        
        misc: {misc}
"""
        chat_memory = ChatMemory(persona=base_persona, human=f"Name: {user_name}", limit=6000)

        # We can try to create an agent and populate a db record for character_id -> agent id

        agent_id = self.agent_client.get_agent_id(agent_name=character_name)

        # If there is an agent with the name already, grab the id and lets remake it. - def a better way to do this.
        if agent_id:
            self.agent_client.delete_agent(agent_id=agent_id)

        agent_state = self.agent_client.create_agent(name=character_name, memory=chat_memory)
        agent_id = agent_state.id

        if not agent_state.id:
            raise ValueError("Agent state was not populated and should be populated to create character.")

        character = CharacterModel(character_id=character_id,
                                   character_name=character_name,
                                   lore=lore,
                                   appearance=appearance,
                                   misc=misc,
                                   agent_id=agent_id
                                   )

        self.db_session.add(character)
        self.db_session.commit()

        return CharacterCreateResponse(character_id=character_id)

    def get_character(self, character_id: str, character_name: Optional[str] = None) -> CharacterGetResponse:
        # Retrieve record
        character_record = self.db_session.query(CharacterModel).filter(
            CharacterModel.character_id == character_id).first()

        if not character_record:
            raise HTTPException(status_code=404, detail="Character not found")

        # Retrieve attributes from the character_record
        character_id = character_record.character_id
        character_name = character_record.character_name
        lore = character_record.lore
        appearance = character_record.appearance
        misc = character_record.misc

        return CharacterGetResponse(character_id=character_id,
                                    character_name=character_name,
                                    lore=lore,
                                    appearance=appearance,
                                    misc=misc
                                    )

    def update_character(self, character_id: str, character_name: str, lore: str, appearance: str,
                         misc: str) -> CharacterUpdateResponse:
        # Retrieve record
        character_record = self.db_session.query(CharacterModel).filter(CharacterModel.character_id == character_id).first()

        if not character_record:
            raise HTTPException(status_code=404, detail="Character not found")

        # Set attributes only if passed
        if character_name:
            character_record.character_name = character_name

        if lore:
            character_record.lore = lore

        if appearance:
            character_record.appearance = appearance

        if misc:
            character_record.misc = misc

        self.db_session.commit()
        self.db_session.refresh(character_record)  # We don't use the record after so this isn't required.

        return CharacterUpdateResponse(character_id=character_id)

    def delete_character(self, character_id: str) -> CharacterDeleteResponse:
        character_record = self.db_session.query(CharacterModel).filter(CharacterModel.character_id == character_id).first()

        if not character_record:
            raise HTTPException(status_code=404, detail="Character not found")

        character_id = character_record.character_id
        character_name = character_record.character_name

        # TODO(ajanitshimanga): hide guts / direct db access to a DataAccess class rather than in server endpoints.

        self.db_session.delete(character_record)
        self.db_session.commit()

        return CharacterDeleteResponse(character_id=character_id, character_name=character_name)

    def list_characters(self, user_id: str):
        raise NotImplementedError

    def send_message(self, character_id: str, message: str, character_name: Optional[str] = None):

        character_record = self.db_session.query(CharacterModel).filter(CharacterModel.character_id == character_id).first()

        agent_id = character_record.agent_id

        # Send message.
        agent_response = self.agent_client.send_message(message=message, role="user", agent_id=agent_id)

        return agent_response


# Database dependency for FastAPI
def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


# Letta dependency for agents
def get_letta_client():
    from letta import create_client

    letta_client = create_client()
    return letta_client


# Service instance using the stubbed database
def get_percy_server(db_session: Session = Depends(get_db_session),
                     letta_client: AbstractClient = Depends(get_letta_client())) -> PercyManagementContext:

    # TODO(ajanitshimanga): refactor with functional mstore dependency
    return PercyManagementContext(db_session, letta_client)


def get_local_percy_server():
    db_session = SessionLocal()
    letta_client = get_letta_client()
    return PercyManagementContext(db_session, letta_client)
