from sqlalchemy import Column, String, DateTime
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

    character_id = Column(String, index=True, primary_key=True)
    character_name = Column(String)
    lore = Column(String)
    appearance = Column(String)
    misc = Column(String)

    # TODO(ajanitshimanga): Handle user based authentication after CRUD.
    # user_id = Column(String, primary_key=True, index=True)
    # past = Column(String)
    # abilities = Column(JSON)
    #
    # weakness = Column(String)
    # strengths = Column(String)
    # affiliations = Column(String)
    # phrases = Column(ARRAY(String))
    # interests = Column(ARRAY(String))
    # relationships = Column(JSON)

    def __repr__(self):
        return (
            f"<Character("
            f"character_id={self.character_id}, "
            f"character_name='{self.character_name}', "
            f"appearance='{self.appearance}', "
            f"lore='{self.lore}', "
            f"misc='{self.misc}', "
        )
