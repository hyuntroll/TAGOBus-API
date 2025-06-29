

class TAGOAPIError(Exception):
    """TAGO API 사용중 생기는 일반적인"""
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
