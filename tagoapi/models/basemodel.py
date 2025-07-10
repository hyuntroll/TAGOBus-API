

class BaseModel:
    def __init__(self): ...

    def to_dict(self) -> dict: ...

    @classmethod
    def from_dict(cls, data:dict) -> "BaseModel": ...

    @classmethod
    def from_list(cls, data:list) -> list["BaseModel"]:
        return [cls.from_dict(v) for v in data]
    
    @property
    def cache_key(self):
        return "BaseModel:<id>"
    

