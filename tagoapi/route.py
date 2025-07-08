from .client import TAGOClient
from .models import Route
from .models import Station
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
    ) -> list[Route]:
        endpoint = f'{self.SERVICE_URL}/getRouteNoList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeNo": routeNo
            }
        )

        res = self.get(endpoint, params=params)
        if res["totalCount"] == 0:
            return []
        route_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
        return Route.from_list(route_list)
    
    @from_cache_or_fetch(604800)
    def get_stations_by_route(
        self,
        cityCode: int,
        routeId: str
    ) -> list[Route]:
        endpoint = f'{self.SERVICE_URL}/getRouteAcctoThrghSttnList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeId": routeId
            }
        )
        res = self.get(endpoint=endpoint, params=params)
        if res["totalCount"] == 0:
            return []
        station_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
        return Station.from_list(station_list)
    
    @from_cache_or_fetch(604800)
    def get_route_info(
        self,
        cityCode: int,
        routeId: str
    ) -> Route:
        endpoint = f'{self.SERVICE_URL}/getRouteInfoIem'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeId": routeId,
            }
        )
        res = self.get(endpoint=endpoint, params=params)
        if not res["items"]["item"]:
            return None
        route = Route.from_dict(res["items"]["item"])

        return route

