from .auth import TAGOAuth
from .exceptions import *
from .utils import *


class TAGOClient:
    BASE_URL = "http://apis.data.go.kr/1613000"

    def __init__(self, auth: TAGOAuth):

        if not isinstance(auth, TAGOAuth):
            raise TypeError("Expected 'auth' to be an instance of TAGOAuth")
        
        self.auth = auth

    def get(self, endpoint: str, params: dict) -> dict:
        
        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
    

        return response.json()

    def get_city_code(self) -> dict:

        endpoint = 'BusSttnInfoInqireService/getCtyCodeList'
        params = {
                "_type": 'json'
            }

        res = self.get(endpoint=endpoint, params=params)
        return res