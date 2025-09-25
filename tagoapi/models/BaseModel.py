from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tagoapi import TAGOClient

class BaseModel:
    cache_key = "BaseModel:<id>"
    def __init__(self, client: "TAGOClient"):
        self._client = client
          
    def to_dict(self) -> dict: ...

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, data: dict, client: "TAGOClient") -> "BaseModel": ...

    @classmethod
    def from_list(cls, data: list, client: "TAGOClient") -> list["BaseModel"]:
        return [cls.from_dict(v, client) for v in data]
    

