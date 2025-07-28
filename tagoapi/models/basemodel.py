

class BaseModel:
    cache_key = "BaseModel:<id>"
    def __init__(self, client):
        self._client = client

    def to_dict(self) -> dict: ...

    def to_dict(self):
        return {k:v for k, v in vars(self).items() 
                if not k.startswith("_") and not callable(v)
                }

    @classmethod
    def from_dict(cls, data:dict) -> "BaseModel": ...

    @classmethod
    def from_list(cls, data:list) -> list["BaseModel"]:
        return [cls.from_dict(v) for v in data]
    

