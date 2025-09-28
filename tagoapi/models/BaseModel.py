from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tagoapi import TAGOClient
    from tagoapi.models.BaseList import BaseList

class BaseModel:
    cache_key = "BaseModel:<id>"
    def __init__(self):
        self._client = None
          
    def to_dict(self) -> dict: ...

    def to_dict(self):
        return vars(self)

    def set_client(self, client: "TAGOClient"):
        self._client = client

    @classmethod
    def from_dict(cls, data: dict) -> "BaseModel": ...

    @classmethod
    def from_list(cls, data: list) -> "BaseList":
        model = BaseList()
        for element in data:
            model.append(cls.from_dict(element))

        return model
        # return [cls.from_dict(v) for v in data]
    

