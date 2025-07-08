from .exceptions import *
from .utils import *


class TAGOClient:
    BASE_URL = "http://apis.data.go.kr/1613000"

    def __init__(self, auth: TAGOAuth):
        if not isinstance(auth, TAGOAuth):
            raise TypeError("Expected 'auth' to be an instance of TAGOAuth")
        
        self.auth = auth

        # self._cache = Cache()

    def get(self, endpoint: str, params: dict) -> dict:
        
        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
    

        return response.json()
    
    # def _from_cache_with_params(
    #     self, 
    #     endpoint: str, 
    #     params: dict, 
    #     ttl:int = 86400
    # ) -> dict:
        
    #     key = endpoint + "?" + "&".join(
    #         f"{key}={value}" for key, value in params.items()
    #     )
    #     cached = cache.get(key)
    #     if cached:
    #         return cached
    #     else:
    #         return False
