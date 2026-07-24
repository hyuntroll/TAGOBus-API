from tagoapi._internal import HttpTransport


class RouteResource:
    def __init__(self, transport: HttpTransport) -> None:
        self._transport = transport