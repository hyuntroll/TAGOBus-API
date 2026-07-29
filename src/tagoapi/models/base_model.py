from abc import ABC, abstractmethod
from typing import Any, Mapping, TypeVar


BaseModelT = TypeVar("BaseModelT", bound="BaseModel")


class BaseModel(ABC):
    def __init__(self, city_code: int | None):
        self.city_code = city_code

    def to_dict(self) -> dict:
        return {
            key: self._serialize(value)
            for key, value in vars(self).items()
            if not key.startswith("_")
        }

    @classmethod
    @abstractmethod
    def from_dict(
        cls: type[BaseModelT],
        data: Mapping[str, Any],
    ) -> BaseModelT:
        raise NotImplementedError

    @staticmethod
    def _serialize(value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.to_dict()
        if isinstance(value, list):
            return [BaseModel._serialize(element) for element in value]
        if isinstance(value, tuple):
            return tuple(BaseModel._serialize(element) for element in value)
        if isinstance(value, dict):
            return {
                key: BaseModel._serialize(element)
                for key, element in value.items()
            }
        return value
