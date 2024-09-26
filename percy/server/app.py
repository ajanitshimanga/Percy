import os

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from percy.metadata_store import CharacterModel
from percy.schemas.characters import CharacterCreateResponse, CharacterCreateRequest

app = FastAPI()

POSTGRES_USER = os.getenv("POSTGRES_USER", "percy")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "percy-password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "percy-db")


# Database setup
# Update with your DB URL TODO(ajanitshimanga): Change to be db agnostic with a db provider factory.
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new character
# TODO(ajanitshimanga): Break out direct database use into a server instance that can make a rewuest to commit a char.
@app.post("/characters/", response_model=CharacterCreateResponse)
def create_character(character: CharacterCreateRequest, db: Session = Depends(get_db)):
    db_character = CharacterModel(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


# class CharacterReadRequest(BaseModel):
#     id: UUID = str(uuid.uuid4())
#
#     class Config:
#         orm_mode = True
#
#
# class CharacterReadResponse(BaseModel):


#TODO(ajanitshimanga): Add in other endpoints later.
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
# # Delete a character
# @app.delete("/characters/{character_id}", response_model=CharacterDeleteResponse)
# def delete_character(character_id: UUID, db: Session = Depends(get_db)):
#     db_character = db.query(CharacterModel).filter(CharacterModel.id == character_id).first()
#     if not db_character:
#         raise HTTPException(status_code=404, detail="Character not found")
#
#     db.delete(db_character)
#     db.commit()
#     return db_character
