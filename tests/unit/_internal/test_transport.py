from unittest.mock import MagicMock

import httpx
import pytest

from tagoapi._internal.transport import HttpTransport
from tagoapi.exceptions import TagoRequestTimeoutError, TagoTransportError


def _response(*, status_code: int = 200, json: dict | None = None) -> httpx.Response:
    return httpx.Response(
        status_code,
        json=json,
        request=httpx.Request("GET", "https://example.test/resource"),
    )


def test_transport_injects_service_key_without_overwriting_explicit_value():
    transport = HttpTransport(
        base_url="https://example.test",
        service_key="default-key",
    )
    transport._client = MagicMock()
    transport._client.get.return_value = _response(json={"response": {}})

    transport.request("/resource", params={"serviceKey": "explicit-key"})

    params = transport._client.get.call_args.kwargs["params"]
    assert params["serviceKey"] == "explicit-key"


def test_transport_maps_http_and_timeout_errors():
    transport = HttpTransport(
        base_url="https://example.test",
        service_key="dummy-key",
    )
    transport._client = MagicMock()
    transport._client.get.return_value = _response(status_code=500, json={})

    with pytest.raises(TagoTransportError):
        transport.request("/resource", params={})

    transport._client.get.side_effect = httpx.TimeoutException("timeout")
    with pytest.raises(TagoRequestTimeoutError):
        transport.request("/resource", params={})
