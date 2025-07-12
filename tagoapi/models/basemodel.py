

class BaseModel:
    cache_key = "BaseModel:<id>"
    def __init__(self): ...

    def to_dict(self) -> dict: ...

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, data:dict) -> "BaseModel": ...

    @classmethod
    def from_list(cls, data:list) -> list["BaseModel"]:
        return [cls.from_dict(v) for v in data]
    

