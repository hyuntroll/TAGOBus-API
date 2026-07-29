from unittest.mock import MagicMock

import httpx
import pytest

from tagoapi._internal.transport import HttpTransport
from tagoapi.exceptions import (
    DeadLineHasExpired,
    NoOpenAPIServiceError,
    OpenAPIApplicationError,
    OpenAPIHTTPError,
    RequestExcessdsError,
    RequestLimitExceededError,
    ServiceAccessDeniedError,
    ServiceKeyNotRegisteredError,
    TagoDecodeError,
    TagoHTTPStatusError,
    TagoOpenAPIError,
    TagoRequestTimeoutError,
    TagoTransportError,
    UnRegisteredIpError,
    UnregisteredIPError,
    UnknownOpenAPIError,
    UsagePeriodExpiredError,
)


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

    with pytest.raises(TagoHTTPStatusError) as exc_info:
        transport.request("/resource", params={})
    assert exc_info.value.status_code == 500

    transport._client.get.side_effect = httpx.TimeoutException("timeout")
    with pytest.raises(TagoRequestTimeoutError):
        transport.request("/resource", params={})


@pytest.mark.parametrize(
    ("error_code", "error_type"),
    [
        ("1", OpenAPIApplicationError),
        ("4", OpenAPIHTTPError),
        ("12", NoOpenAPIServiceError),
        ("20", ServiceAccessDeniedError),
        ("22", RequestLimitExceededError),
        ("30", ServiceKeyNotRegisteredError),
        ("31", UsagePeriodExpiredError),
        ("32", UnregisteredIPError),
        ("99", UnknownOpenAPIError),
    ],
)
def test_transport_maps_open_api_error_codes(error_code, error_type):
    transport = HttpTransport(
        base_url="https://example.test",
        service_key="dummy-key",
    )
    transport._client = MagicMock()
    transport._client.get.return_value = _response(json={
        "returnReasonCode": error_code,
        "returnAuthMsg": "SERVICE ERROR",
    })

    with pytest.raises(error_type) as exc_info:
        transport.request("/resource", params={})

    assert exc_info.value.return_reason_code == error_code
    assert exc_info.value.detail == "SERVICE ERROR"


def test_transport_preserves_unknown_open_api_error_code():
    transport = HttpTransport(
        base_url="https://example.test",
        service_key="dummy-key",
    )
    transport._client = MagicMock()
    transport._client.get.return_value = _response(json={
        "returnReasonCode": "777",
    })

    with pytest.raises(TagoOpenAPIError) as exc_info:
        transport.request("/resource", params={})

    assert exc_info.value.return_reason_code == "777"


def test_transport_maps_xml_open_api_error_response():
    transport = HttpTransport(
        base_url="https://example.test",
        service_key="dummy-key",
    )
    transport._client = MagicMock()
    transport._client.get.return_value = httpx.Response(
        200,
        text="""
        <OpenAPI_ServiceResponse>
            <cmmMsgHeader>
                <errMsg>SERVICE ERROR</errMsg>
                <returnAuthMsg>SERVICE_KEY_IS_NOT_REGISTERED_ERROR</returnAuthMsg>
                <returnReasonCode>30</returnReasonCode>
            </cmmMsgHeader>
        </OpenAPI_ServiceResponse>
        """,
        request=httpx.Request("GET", "https://example.test/resource"),
    )

    with pytest.raises(ServiceKeyNotRegisteredError) as exc_info:
        transport.request("/resource", params={})

    assert exc_info.value.return_reason_code == "30"
    assert exc_info.value.detail == "SERVICE_KEY_IS_NOT_REGISTERED_ERROR"


def test_transport_raises_decode_error_for_invalid_payload():
    transport = HttpTransport(
        base_url="https://example.test",
        service_key="dummy-key",
    )
    transport._client = MagicMock()
    transport._client.get.return_value = httpx.Response(
        200,
        text="not-json-or-xml",
        request=httpx.Request("GET", "https://example.test/resource"),
    )

    with pytest.raises(TagoDecodeError):
        transport.request("/resource", params={})


def test_legacy_exception_names_are_compatibility_aliases():
    assert RequestExcessdsError is RequestLimitExceededError
    assert DeadLineHasExpired is UsagePeriodExpiredError
    assert UnRegisteredIpError is UnregisteredIPError
