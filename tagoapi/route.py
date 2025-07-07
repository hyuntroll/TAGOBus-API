from .client import TAGOClient
from .auth import TAGOAuth
from .utils import *


class BusRoute(TAGOClient):
    SERVICE_URL = "BusRouteInfoInqireService"
    
    def __init__(self, auth: TAGOAuth):
        super().__init__(auth) 

    def get_route_list(
        self, 
        cityCode: int,
        routeNo: int,
    ) -> dict:            
        endpoint = f'{self.SERVICE_URL}/getRouteNoList'
        key = f'{endpoint}={cityCode}&routeNo={routeNo}'

        cached = cache.get(key)
        if cached:
            return cached

        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeNo": routeNo,
            }
        ) 

        res = self.get(endpoint=endpoint, params=params)
        cache.save(key, res, ttl=604800)
        return res
    
    def get_stations_by_route(
        self,
        cityCode: int,
        routeId: str,
    ) -> dict:
        
        endpoint = f'{self.SERVICE_URL}/getRouteAcctoThrghSttnList'
        key = f'{endpoint}={cityCode}&routeId={routeId}'
        cached = cache.get(key)
        if cached:
            return cached
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeId": routeId
            }
        ) 

        res = self.get(endpoint=endpoint, params=params)
        cache.save(key, res, ttl=604800)
        return res
    
    def get_route_info(
        self,
        cityCode: int,
        routeId: str,
    ) -> dict:
            
        endpoint = f'{self.SERVICE_URL}/getRouteInfoIem'
        key = f'{endpoint}={cityCode}&routeId={routeId}'
        cached = cache.get(key)
        if cached:
            return cached
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeId": routeId,
            }
        )
        
        res = self.get(endpoint=endpoint, params=params)
        cache.save(key, res, ttl=604800)
        return res
    