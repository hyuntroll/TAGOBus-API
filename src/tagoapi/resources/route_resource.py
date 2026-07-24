from tagoapi._internal.transport import HttpTransport
from .resource import TagoResource


class ArrivalResource(TagoResource):
    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)