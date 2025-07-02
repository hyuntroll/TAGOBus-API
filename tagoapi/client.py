from .exceptions import *
import requests
from .auth import TAGOAuth


class TAGOClient:
    BASE_URL = "http://apis.data.go.kr/1613000"

    def __init__(self, client: TAGOAuth):
        """
        summery
        """
        if not isinstance(client, TAGOAuth):
            raise TypeError("Expected 'client' to be an instance of TAGOClient ")
        
        self.client = client


    def get(self, endpoint: str, params: dict) -> dict:
        params = self.client.apply(params)

        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
    

        return response.json()
        