from abc import abstractmethod

import uvicorn
from app import app


class AbstractPercyContext(object):
    @abstractmethod
    def create_character(self, character_name: str, character_dict: dict):
        raise NotImplementedError

    @abstractmethod
    def get_character(self, character_id: str):
        raise NotImplementedError

    @abstractmethod
    def update_character(self, character_id: str, character_name: str, character_dict: dict):
        raise NotImplementedError

    @abstractmethod
    def delete_character(self, character_id: str):
        raise NotImplementedError

    @abstractmethod
    def list_characters(self):
        raise NotImplementedError


class PercyManagementContext(AbstractPercyContext):

    def __init__(self, letta_client_instance):
        self.letta_client = letta_client_instance

    def create_character(self, character_name: str, character_dict: dict):
        raise NotImplementedError

    def get_character(self, character_id: str):
        raise NotImplementedError

    def update_character(self, character_id: str, character_name: str, character_dict: dict):
        raise NotImplementedError

    def delete_character(self, character_id: str):
        raise NotImplementedError

    def list_characters(self):
        raise NotImplementedError


# Implement concrete PercyManagementContext


if __name__ == "__main__":
    # In production, reload is usually set to False.

    uvicorn.run(app=app, host="127.0.0.1", port=8080, log_level="info")
