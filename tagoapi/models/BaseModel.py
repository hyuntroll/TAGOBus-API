from typing import TYPE_CHECKING
from tagoapi.models.BaseList import BaseList
if TYPE_CHECKING:
    from tagoapi import TAGOClient

class BaseModel:
    cache_key = "BaseModel:<id>"
    def __init__(self):
        self._client = None
          
    def to_dict(self) -> dict:
        return vars(self)

    def set_client(self, client: "TAGOClient"):
        self._client = client

    @classmethod
    def from_dict(cls, data: dict) -> "BaseModel": ...

    @classmethod
    def from_list(cls, data: list) -> BaseList:
        return BaseList([cls.from_dict(d) for d in data])
        # model = BaseList()
        # for element in data:
        #     model.append(cls.from_dict(element))
        #
        # return model

    

