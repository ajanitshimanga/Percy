from fastapi import FastAPI, Depends

from percy.schemas.characters import CharacterCreateResponse, CharacterCreateRequest, CharacterDeleteResponse, \
    CharacterGetRequest, CharacterGetResponse, CharacterUpdateRequest, CharacterUpdateResponse
from percy.server.server import get_percy_server


def create_application() -> FastAPI:
    fast_api_app = FastAPI()

    # TODO(ajanitshimanga): Add middleware and http header stubbing.

    return fast_api_app


# Initialize app
app = create_application()


# Create a new character
@app.post("/characters/", response_model=CharacterCreateResponse)
def create_character(request: CharacterCreateRequest, percy_server: Depends(get_percy_server)):
    character_id = request.character_id
    name = request.name
    lore = request.lore
    appearance = request.appearance
    misc = request.misc

    response = percy_server.create_character(character_id=character_id,
                                             character_name=name,
                                             lore=lore,
                                             appearance=appearance,
                                             misc=misc)

    return response


# Update a character
@app.patch("/characters/{character_id}", response_model=CharacterUpdateResponse)
def update_character(request: CharacterUpdateRequest, percy_server: Depends(get_percy_server)):
    character_id = request.character_id
    character_name = request.character_name
    lore = request.lore
    appearance = request.appearance
    misc = request.misc

    response = percy_server.update_character(character_id=character_id,
                                             character_name=character_name,
                                             lore=lore,
                                             appearance=appearance,
                                             misc=misc
                                             )
    return response


# Get a character
@app.get("/characters/", response_model=CharacterGetResponse)
def get_character(request: CharacterGetRequest, percy_server: Depends(get_percy_server)):
    character_id = request.character_id
    character_name = request.character_name

    response = percy_server.get_character(character_id=character_id,
                                          character_name=character_name
                                          )

    return response


# Delete a character
@app.delete("/characters/{character_id}", response_model=CharacterDeleteResponse)
def delete_character(character_id: str, percy_server: Depends(get_percy_server)):
    response = percy_server.delete_character(character_id=character_id)

    return response
