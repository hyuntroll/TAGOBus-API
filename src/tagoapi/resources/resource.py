from tagoapi._internal.transport import HttpTransport
from tagoapi.utils import parse_metadata


class TagoResource:
    middle_path: str
    def __init__(self, transport: HttpTransport) -> None:
        self._transport = transport

    def _request(
            self,
            path: str,
            params: dict
    ) -> dict:
        request_path = self.middle_path + path
        response = parse_metadata(
            self._transport.request(
            request_path,
            params=params,)
        )
        return {} if response is None else response