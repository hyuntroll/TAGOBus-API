from typing import Any, Mapping

from .base_model import BaseModel


class CityCode(BaseModel):
    def __init__(self, city_code: int, city_name: str):
        super().__init__(city_code)
        self.city_name = city_name

    def __repr__(self) -> str:
        return f"CityCode({self.city_code}, {self.city_name!r})"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CityCode":
        city_code = data.get("citycode")
        city_name = data.get("cityname")
        if city_code is None or city_code == "":
            raise ValueError("citycode는 필수입니다.")
        if city_name is None or city_name == "":
            raise ValueError("cityname은 필수입니다.")
        return cls(city_code=int(city_code), city_name=str(city_name))
