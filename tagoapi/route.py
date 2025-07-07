from .client import TAGOClient
from .auth import TAGOAuth
from .utils import *


class BusRoute(TAGOClient):
    SERVICE_URL = "BusRouteInfoInqireService"
    
    def __init__(self, auth: TAGOAuth):
        super().__init__(auth) 

    @from_cache_or_fetch(604800)
    def get_route_list(
        self,
        cityCode: int,
        routeNo: int
    ) -> dict:
        endpoint = f'{self.SERVICE_URL}/getRouteNoList'
        
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeNo": routeNo
            }
        )
        res = self.get(endpoint, params=params)

        return res
    

    @from_cache_or_fetch(604800)
    def get_stations_by_route(
        self,
        cityCode: int,
        routeId: str
    ) -> dict:
        endpoint = f'{self.SERVICE_URL}/getRouteAcctoThrghSttnList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeId": routeId
            }
        ) 
        res = self.get(endpoint=endpoint, params=params)

        return res
    

    @from_cache_or_fetch(604800)
    def get_route_info(
        self,
        cityCode: int,
        routeId: str
    ) -> dict:
        endpoint = f'{self.SERVICE_URL}/getRouteInfoIem'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeId": routeId,
            }
        )
        
        res = self.get(endpoint=endpoint, params=params)
        return res
    