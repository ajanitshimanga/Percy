from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()


# Pydantic Model for User
class User(BaseModel):
    id: str
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


# SQLAlchemy Model for User
class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True))

    def __repr__(self) -> str:
        return f"<User(id='{self.id}', username='{self.username}')>"

    def to_record(self) -> User:
        return User(id=self.id, username=self.username, created_at=self.created_at)


# SQLAlchemy Model for Character
class CharacterModel(Base):
    __tablename__ = "characters"
    __table_args__ = {"extend_existing": True}

    user_id = Column(String, primary_key=True, index=True)
    character_id = Column(String, index=True)
    character_name = Column(String)
    lore = Column(String)
    past = Column(String)
    appearance = Column(String)
    abilities = Column(JSON)

    weakness = Column(String)
    strengths = Column(String)
    affiliations = Column(String)
    phrases = Column(ARRAY(String))
    interests = Column(ARRAY(String))
    relationships = Column(JSON)

    def __repr__(self):
        return (
            f"<Character("
            f"user_id={self.user_id}, "
            f"character_id={self.character_id}, "
            f"character_name='{self.character_name}', "
            f"lore='{self.lore}', "
            f"past='{self.past}', "
            f"appearance='{self.appearance}', "
            f"abilities={self.abilities}, "
            f"weakness='{self.weakness}', "
            f"strengths='{self.strengths}', "
            f"affiliations='{self.affiliations}', "
            f"phrases={self.phrases}, "
            f"interests={self.interests}, "
            f"relationships={self.relationships})>"
        )
