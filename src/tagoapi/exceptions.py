class TagoAPIError(Exception):
    """모든 TAGO API 예외의 기반 클래스."""


class TagoTransportError(TagoAPIError):
    """HTTP 통신 또는 응답 디코딩 실패."""


class TagoRequestTimeoutError(TagoTransportError):
    """TAGO API 요청 시간 초과."""


class TagoHTTPStatusError(TagoTransportError):
    """TAGO API가 실패 HTTP 상태를 반환한 경우."""

    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"TAGO API HTTP 오류: {status_code}")


class TagoDecodeError(TagoTransportError):
    """응답을 JSON 또는 XML로 디코딩할 수 없는 경우."""


class TagoResponseError(TagoAPIError):
    """TAGO 응답 형식이 문서 규격과 다른 경우."""


class TagoServiceError(TagoResponseError):
    """제공기관이 정상 결과 코드가 아닌 응답을 반환한 경우."""

    def __init__(self, result_code: str, result_message: str | None = None):
        self.result_code = str(result_code)
        self.result_message = result_message
        message = f"TAGO 서비스 오류: {self.result_code}"
        if result_message:
            message = f"{message} {result_message}"
        super().__init__(message)


class InvalidRequestParameterError(TagoServiceError):
    """제공기관 오류 코드 99: 잘못된 요청 파라미터."""


class TagoOpenAPIError(TagoAPIError):
    """공공데이터포털 OpenAPI 오류 응답."""

    default_message = "공공데이터포털 오류가 발생했습니다."

    def __init__(
        self,
        return_reason_code: str,
        detail: str | None = None,
    ):
        self.return_reason_code = str(return_reason_code)
        self.detail = detail
        message = (
            f"{self.default_message} "
            f"(returnReasonCode={self.return_reason_code})"
        )
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)


class OpenAPIApplicationError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 1."""

    default_message = "공공데이터포털 애플리케이션 오류가 발생했습니다."


class OpenAPIHTTPError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 4."""

    default_message = "공공데이터포털 HTTP 오류가 발생했습니다."


class NoOpenAPIServiceError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 12."""

    default_message = "해당 OpenAPI 서비스가 없거나 폐기되었습니다."


class ServiceAccessDeniedError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 20."""

    default_message = "OpenAPI 서비스 접근이 거부되었습니다."


class RequestLimitExceededError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 22."""

    default_message = "OpenAPI 서비스 요청 제한 횟수를 초과했습니다."


class ServiceKeyNotRegisteredError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 30."""

    default_message = "등록되지 않은 서비스 키입니다."


class UsagePeriodExpiredError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 31."""

    default_message = "OpenAPI 활용 기간이 만료되었습니다."


class UnregisteredIPError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 32."""

    default_message = "등록되지 않은 IP입니다."


class UnknownOpenAPIError(TagoOpenAPIError):
    """공공데이터포털 오류 코드 99."""

    default_message = "공공데이터포털에서 알 수 없는 오류를 반환했습니다."


# 기존 공개 이름은 다음 major 버전까지 호환 alias로 유지한다.
TAGOAPIError = TagoAPIError
RequestExcessdsError = RequestLimitExceededError
DeadLineHasExpired = UsagePeriodExpiredError
UnRegisteredIpError = UnregisteredIPError


__all__ = [
    "TagoAPIError",
    "TagoTransportError",
    "TagoRequestTimeoutError",
    "TagoHTTPStatusError",
    "TagoDecodeError",
    "TagoResponseError",
    "TagoServiceError",
    "InvalidRequestParameterError",
    "TagoOpenAPIError",
    "OpenAPIApplicationError",
    "OpenAPIHTTPError",
    "NoOpenAPIServiceError",
    "ServiceAccessDeniedError",
    "RequestLimitExceededError",
    "ServiceKeyNotRegisteredError",
    "UsagePeriodExpiredError",
    "UnregisteredIPError",
    "UnknownOpenAPIError",
    "TAGOAPIError",
    "RequestExcessdsError",
    "DeadLineHasExpired",
    "UnRegisteredIpError",
]
