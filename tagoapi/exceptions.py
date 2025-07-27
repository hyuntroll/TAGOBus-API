

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

class NoOpenAPIServiceError(TAGOAPIError):
    """오픈 API 서비스가 없거나 페기됨"""
    pass

class TAGORequestError(TAGOAPIError):
    """요청 실패 (http 에러, 타임아웃 등)"""
    def __init__(self, message: str, status_code: int | None ):
        super().__init__(message)
        self.status_code = status_code

class TAGOResponseError(TAGOAPIError):
    """ 요청 오류 """
    def __init__(self, message: str, status_code: int | None ):
        super().__init__(message)
        self.status_code = status_code
