from typing import Any

import httpx
import xmltodict

from tagoapi.exceptions import (
    NoOpenAPIServiceError,
    OpenAPIApplicationError,
    OpenAPIHTTPError,
    RequestLimitExceededError,
    ServiceAccessDeniedError,
    ServiceKeyNotRegisteredError,
    TagoDecodeError,
    TagoHTTPStatusError,
    TagoOpenAPIError,
    TagoRequestTimeoutError,
    TagoServiceError,
    TagoTransportError,
    UnknownOpenAPIError,
    UnregisteredIPError,
    UsagePeriodExpiredError,
)


class HttpTransport:
    _OPEN_API_ERRORS = {
        "1": OpenAPIApplicationError,
        "4": OpenAPIHTTPError,
        "12": NoOpenAPIServiceError,
        "20": ServiceAccessDeniedError,
        "22": RequestLimitExceededError,
        "30": ServiceKeyNotRegisteredError,
        "31": UsagePeriodExpiredError,
        "32": UnregisteredIPError,
        "99": UnknownOpenAPIError,
    }

    def __init__(
        self,
        *,
        base_url: str,
        service_key: str,
    ) -> None:
        self._service_key = service_key
        self._client = httpx.Client(
            base_url=base_url,
        )

    def close(self) -> None:
        self._client.close()

    def request(
        self,
        path: str,
        *,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        request_params = dict(params or {})
        request_params.setdefault("serviceKey", self._service_key)
        try:
            response = self._client.get(
                path,
                params=request_params,
                timeout=httpx.Timeout(10.0, connect=3.0),
            )
        except httpx.TimeoutException as exc:
            raise TagoRequestTimeoutError(
                "API 요청 시간이 초과되었습니다."
            ) from exc
        except httpx.RequestError as exc:
            raise TagoTransportError(
                "API 서버와 통신하지 못했습니다."
            ) from exc

        self._raise_for_status(response)

        return self._parse_response(response)

    def _raise_for_status(self, response: httpx.Response) -> None:
        status = response.status_code
        if status >= 400:
            raise TagoHTTPStatusError(status)

    def _parse_response(
        self,
        response: httpx.Response,
    ) -> dict[str, Any]:
        payload = self._parse_payload(response)
        self._raise_for_return_reason(payload)
        return payload

    def _parse_payload(
        self,
        response: httpx.Response,
    ) -> dict[str, Any]:
        try:
            payload = response.json()
            if not isinstance(payload, dict):
                raise TagoDecodeError("TAGO 응답 최상위 값은 객체여야 합니다.")
            return payload
        except ValueError as exc:
            try:
                parsed_xml = xmltodict.parse(response.text)
                open_api_error = parsed_xml.get("OpenAPI_ServiceResponse")
                if isinstance(open_api_error, dict):
                    return open_api_error.get("cmmMsgHeader", open_api_error)
                return parsed_xml
            except Exception as parse_exc:
                raise TagoDecodeError(
                    "TAGO 응답을 JSON 또는 XML로 디코딩할 수 없습니다."
                ) from parse_exc

    def _raise_for_return_reason(
        self,
        payload: dict[str, Any],
    ) -> None:
        error_code = payload.get("returnReasonCode")
        if not error_code:
            header = payload.get("header") or payload.get("cmmMsgHeader")
            if isinstance(header, dict):
                response_code = header.get("resultCode")
                response_msg = header.get("resultMsg")
                if response_code and str(response_code) != "00":
                    raise TagoServiceError(
                        str(response_code),
                        None if response_msg is None else str(response_msg),
                    )
            return

        error_code = str(error_code)
        error_type = self._OPEN_API_ERRORS.get(error_code, TagoOpenAPIError)
        detail = payload.get("returnAuthMsg") or payload.get("errMsg")
        raise error_type(
            error_code,
            None if detail is None else str(detail),
        )
