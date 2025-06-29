from .exceptions import *
import requests


class TAGOClient:
    BASE_URL = "http://apis.data.go.kr/1613000"

    def __init__(self, serviceKey: str):
        """
        summery
        """
        self.serviceKey = serviceKey


    def get(self, endpoint: str, params: dict) -> dict:
        params["serviceKey"] = self.serviceKey

        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
    

        return response.json()
        