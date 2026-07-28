from abc import ABC, abstractmethod
from typing import Any, ClassVar, Mapping, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from tagoapi.client import TAGOClient


BaseModelT = TypeVar("BaseModelT", bound="BaseModel")
_UNSET = object()


class BaseModel(ABC):
    _lazy_fields: ClassVar[dict[str, str]] = {}

    def __init__(self, city_code: int | None):
        object.__setattr__(self, "_client", None)
        object.__setattr__(self, "_loading_lazy_groups", set())
        object.__setattr__(self, "_lazy_values", {})
        self.city_code = city_code

    def __setattr__(self, name: str, value: Any) -> None:
        if name in type(self)._lazy_fields:
            lazy_values = self.__dict__.get("_lazy_values")
            if lazy_values is not None:
                if value is None:
                    lazy_values[name] = _UNSET
                    self.__dict__.pop(name, None)
                    return
                lazy_values[name] = value

        object.__setattr__(self, name, value)

    def __getattr__(self, field_name: str) -> Any:
        if field_name in type(self)._lazy_fields:
            return self._load_lazy_field(field_name)

        raise AttributeError(
            f"{type(self).__name__} has no attribute {field_name}"
        )

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

    def bind_client(self: BaseModelT, client: "TAGOClient") -> BaseModelT:
        object.__setattr__(self, "_client", client)
        return self

    def is_loaded(self, field_name: str) -> bool:
        self._validate_lazy_field(field_name)
        return self._lazy_values.get(field_name, _UNSET) is not _UNSET

    def load(self, field_name: str) -> Any:
        self._validate_lazy_field(field_name)
        if self.is_loaded(field_name):
            return self.__dict__[field_name]

        return self._load_lazy_field(field_name)

    def refresh(self, field_name: str) -> Any:
        self._validate_lazy_field(field_name)
        for grouped_field in self._lazy_group_fields(field_name):
            self._lazy_values[grouped_field] = _UNSET
            self.__dict__.pop(grouped_field, None)

        return self._load_lazy_field(field_name)

    def _load_lazy_field(self, field_name: str) -> Any:
        self._validate_lazy_field(field_name)
        if self.is_loaded(field_name):
            return self.__dict__[field_name]

        client = self._client
        if client is None:
            raise RuntimeError(
                f"{type(self).__name__}.{field_name} cannot be loaded without client"
            )

        loader_name = type(self)._lazy_fields[field_name]
        loading_groups = self._loading_lazy_groups
        if loader_name in loading_groups:
            raise RuntimeError(
                f"Circular lazy loading detected for "
                f"{type(self).__name__}.{field_name}"
            )

        loading_groups.add(loader_name)
        try:
            loader = getattr(client, loader_name)
            loaded_value = loader(self)

            if isinstance(loaded_value, type(self)):
                for grouped_field in self._lazy_group_fields(field_name):
                    self._store_lazy_value(
                        grouped_field,
                        loaded_value.__dict__.get(grouped_field),
                    )
            else:
                self._store_lazy_value(field_name, loaded_value)

            if field_name not in self.__dict__:
                self._store_lazy_value(field_name, None)

            return self.__dict__[field_name]
        finally:
            loading_groups.remove(loader_name)

    def _lazy_group_fields(self, field_name: str) -> tuple[str, ...]:
        loader_name = type(self)._lazy_fields[field_name]
        return tuple(
            name
            for name, configured_loader in type(self)._lazy_fields.items()
            if configured_loader == loader_name
        )

    def _store_lazy_value(self, field_name: str, value: Any) -> None:
        self._lazy_values[field_name] = value
        object.__setattr__(self, field_name, value)

    def _validate_lazy_field(self, field_name: str) -> None:
        if field_name not in type(self)._lazy_fields:
            raise AttributeError(
                f"{type(self).__name__}.{field_name} is not a lazy field"
            )

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
