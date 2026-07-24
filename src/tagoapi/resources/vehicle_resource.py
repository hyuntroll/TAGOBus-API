from tagoapi._internal.transport import HttpTransport


class VehicleResource:
    def __init__(self, transport: HttpTransport) -> None:
        self._transport = transport