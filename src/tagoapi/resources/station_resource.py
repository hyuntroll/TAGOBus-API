from tagoapi._internal import HttpTransport


class StationResource:
    def __init__(self, transport: HttpTransport) -> None:
        self._transport = transport