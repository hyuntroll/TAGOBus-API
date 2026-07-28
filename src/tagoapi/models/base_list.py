from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tagoapi.client import TAGOClient
    from tagoapi.models.base_model import BaseModel

class BaseList(list):

    def as_list(self) -> list["BaseModel"]:
        return list(self)

    def set_client(self, client: "TAGOClient") -> "BaseList":
        for element in self:
            element.set_client(client)

        return self
