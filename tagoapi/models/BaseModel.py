from typing import TYPE_CHECKING
from tagoapi.models.BaseList import BaseList
if TYPE_CHECKING:
    from tagoapi import TAGOClient

class BaseModel:
    cache_key = "BaseModel:<id>"
    _lazy_fields: dict = {}

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

    def __getattr__(self, item):

        if item in self._lazy_fields:
            if self._client is None:
                raise RuntimeError(f"{self.__class__.__name__} cannot be loaded without client")

            _client = self._client
            loader = getattr(_client, self._lazy_fields[item])
            loaded_value = loader(self)

            # 같은 개체라면 | 속성 저장
            if isinstance(loaded_value, self.__class__):
                for k, v in loaded_value.to_dict().items():

                    if not k.startswith("_"):
                        setattr(self, k, v)
            else: # 다른 개체라면 item = loaded_value
                setattr(self, item, loaded_value)

            return self.__dict__[item]


        raise AttributeError(f"{self.__class__.__name__} has no attribute {item}")


    ## 모든 속성에 접근할 때 가장 먼저 호출되는 메서드
    ## 구현할 때 없으면 raise 땡기고, 거기서 만약 인스턴스 두개가 다르면 그거 자체를 속성으로 저장하고 같으면 속성을 하나씩 저장하게
    def __getattribute__(self, item):
        if super().__getattribute__(item) is not None:
            return super().__getattribute__(item)
        if super().__getattribute__("_client") is None:
            raise RuntimeError(f"{self.__class__.__name__} cannot be loaded without client")

        raise AttributeError(f"{self.__class__.__name__} object has no attribute {item}")

