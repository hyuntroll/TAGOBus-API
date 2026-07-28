

class TAGOAPIError(Exception):
    """TAGO API 사용중 생기는 일반적인 오류"""
    pass
class UtilError(Exception):
    """Utils 사용 중 생긴 오류"""
    pass
class TagoRequestTimeoutError(TAGOAPIError):
    """API 요청 시간 초과"""
    pass
class TagoTransportError(TAGOAPIError):
    """API 서버 통신 실패"""
    pass


class TagoResponseError(TAGOAPIError):
    """TAGO 응답 형식이 문서 규격과 다를 때 발생하는 오류."""


class TagoServiceError(TagoResponseError):
    """TAGO 서비스가 정상 결과 코드가 아닌 응답을 반환한 경우."""

    def __init__(self, result_code: str, result_message: str | None = None):
        self.result_code = result_code
        self.result_message = result_message
        message = f"TAGO 서비스 오류: {result_code}"
        if result_message:
            message = f"{message} {result_message}"
        super().__init__(message)
class ServiceKeyNotRegisteredError(TAGOAPIError):
    """등록되지 않은 서비스키를 사용"""
    pass
class RequestExcessdsError(TAGOAPIError):
    """서비스 요청제한횟수 초과 에러"""
    pass

class DeadLineHasExpired(TAGOAPIError):
    """활용기간 만료"""
    pass

class UnRegisteredIpError(TAGOAPIError):
    """등록되지 않은 IP"""
    pass

class ServiceAccessDeniedError(TAGOAPIError):
    """서비스 접근 거부"""

class NoOpenAPIServiceError(TAGOAPIError):
    """오픈 API 서비스가 없거나 페기됨"""
    pass
class CacheNotFoundError(TAGOAPIError):
    """캐시파일을 불러오지 못할 때"""
    pass
