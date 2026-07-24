import httpx
import xmltodict

from tagoapi.exceptions import (
    RequestExcessdsError,
    ServiceAccessDeniedError,
    ServiceKeyNotRegisteredError,
    TagoRequestTimeoutError,
    TagoTransportError,
    NoOpenAPIServiceError,
    UnRegisteredIpError,
    DeadLineHasExpired,
)


class HttpTransport:
    def __init__(
            self,
            *,
            base_url: str,
            service_key: str
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
            * ,
            params: dict
    ) -> dict:
        request_params = dict(params or {})
        request_params.setdefault("serviceKey", self._service_key)
        try:
            response = self._client.get(path, params=request_params, timeout=(3.0, 10.0))
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
            raise TagoTransportError(f"HTTP 오류 발생: {status}")

    def _parse_response(self, response: httpx.Response) -> dict:
        payload = self._parse_payload(response)
        self._raise_for_return_reason(payload)
        return payload

    def _parse_payload(self, response: httpx.Response) -> dict:
        try:
            return response.json()
        except ValueError as exc:
            try:
                parsed_xml = xmltodict.parse(response.text)
                open_api_error = parsed_xml.get("OpenAPI_ServiceResponse")
                if isinstance(open_api_error, dict):
                    return open_api_error.get("cmmMsgHeader", open_api_error)
                return parsed_xml
            except Exception as parse_exc:
                raise ValueError("응답을 JSON으로 디코딩 할 수 없습니다.") from parse_exc

    def _raise_for_return_reason(self, payload: dict) -> None:
        error_code = payload.get("returnReasonCode")
        if not error_code:
            header = payload.get("header") or payload.get("cmmMsgHeader")
            if isinstance(header, dict):
                response_code = header.get("resultCode")
                response_msg = header.get("resultMsg")
                if response_code and str(response_code) != "00":
                    raise TagoTransportError(f"응답 오류: {response_code} {response_msg}")
            return

        error_code = str(error_code)

        if error_code == "4":
            raise TagoTransportError("HTTP 에러가 발생했습니다.")
        if error_code == "12":
            raise NoOpenAPIServiceError("해당 오픈 API 서비스가 없거나 폐기된 서비스입니다.")
        if error_code == "20":
            raise ServiceAccessDeniedError("서비스에 접근이 거부되었습니다.")
        if error_code == "22":
            raise RequestExcessdsError("서비스 요청제한횟수를 초과했습니다.")
        if error_code == "30":
            raise ServiceKeyNotRegisteredError("유효하지 않는 서비스키 입니다.")
        if error_code == "31":
            raise DeadLineHasExpired("API활용기간이 만료되었습니다.")
        if error_code == "32":
            raise UnRegisteredIpError("등록되지 않은 IP입니다.")
        if error_code == "99":
            raise TagoTransportError("요청 파라미터가 잘못되었습니다.")
        raise RuntimeError(f"실행중 오류가 발생했습니다. 에러코드: {error_code}")
