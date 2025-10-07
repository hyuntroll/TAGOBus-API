from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tagoapi.models.BaseModel import BaseModel
    from tagoapi import TAGOClient

class BaseList(list):

    def as_list(self) -> list["BaseModel"]:
        return list(self)

    def set_client(self, client: "TAGOClient"):
        for element in self:
            element.set_client(client)

        return self