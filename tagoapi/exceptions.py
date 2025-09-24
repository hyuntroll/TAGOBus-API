

class TAGOAPIError(Exception):
    """TAGO API 사용중 생기는 일반적인"""
    pass

class UtilError(Exception):
    """Utils 사용 중 생긴 오류"""
    pass
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

