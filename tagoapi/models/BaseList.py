from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tagoapi.models.BaseModel import BaseModel
    from tagoapi import TAGOClient

class BaseList(list): # list 상속 받아도 좋을듯

    def as_list(self) -> list["BaseModel"]:
        return list(self)

    def set_client(self, client: "TAGOClient"):
        for element in self:
            element.set_client(client)

        return self