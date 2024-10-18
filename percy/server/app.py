import os
import uuid

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

#from percy.metadata_store import CharacterModel
from percy.schemas.characters import CharacterCreateResponse, CharacterCreateRequest, CharacterDeleteResponse, \
    CharacterGetRequest, CharacterGetResponse
from percy.server.server import get_percy_server


app = FastAPI()


# Create a new character
# TODO(ajanitshimanga): Break out direct database use into a server instance that can make a rewuest to commit a char.
@app.post("/characters/", response_model=CharacterCreateResponse)
def create_character(character: CharacterCreateRequest, percy_server: Depends(get_percy_server)):

    character_id = character.character_id
    name = character.name
    lore = character.lore
    appearance = character.appearance
    misc = character.misc

    percy_server.create_character(character_id=character_id,
                                  character_name=name,
                                  lore=lore,
                                  appearance=appearance,
                                  misc=misc)

    return CharacterCreateResponse(character_id=character_id)


# Get a character
# TODO(ajanitshimanga): Break out direct database use into a server instance that can make a rewuest to commit a char.
@app.post("/characters/", response_model=CharacterGetResponse)
def get_character(request: CharacterGetRequest, percy_server: Depends(get_percy_server)):

    response = percy_server.get_character(character_id=request.character_id, character_name=request.character_name)
    return response




# Delete a character
@app.delete("/characters/{character_id}", response_model=CharacterDeleteResponse)
def delete_character(character_id: str, percy_server: Depends(get_percy_server)):

    character_name = percy_server.delete_character(character_id=character_id)

    return CharacterDeleteResponse(character_id=character_id, character_name=str(character_name))


# TODO(ajanitshimanga): Add in other endpoints later.

# # Read a character based on id
# @app.get("/characters/{user_id}")
# def get_character(character_read: CharacterGetRequest, db: Session = next(get_db())):



# class CharacterReadRequest(BaseModel):
#     id: UUID = str(uuid.uuid4())
#
#     class Config:
#         orm_mode = True
#
#
# class CharacterReadResponse(BaseModel):


# TODO(ajanitshimanga): Add in other endpoints later.
#
# # Read all characters
# @app.get("/characters/{user_id}", response_model=List[CharacterReadResponse])
# def list_characters(user_id: UUID, skip: int = 0, limit: int = 10, db: Session = next(get_db())):
#     return db.query(CharacterModel).offset(skip).limit(limit).all()
#
#
# # Update a character
# @app.put("/characters/{character_id}", response_model=CharacterReadResponse)
# def update_character(character_id: UUID, character: CharacterCreateRequest, db: Session = Depends(get_db)):
#     db_character = db.query(CharacterModel).filter(CharacterModel.id == character_id).first()
#     if not db_character:
#         raise HTTPException(status_code=404, detail="Character not found")
#
#     for key, value in character.dict().items():
#         setattr(db_character, key, value)
#
#     db.commit()
#     db.refresh(db_character)
#     return db_character
#
#
