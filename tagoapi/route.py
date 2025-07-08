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

        data_lst = res["response"]["body"]["items"]["item"]
        if isinstance(data_lst, dict):
            data_lst = [data_lst]

        route_lst = [] 
        for data in data_lst: # 이거 값이 하나일 때랑 여러개일 때 파일이 다름 하나일 땐 dict, list[dict] 이렇게 되서 이거 고치면 될듯
            # print(data)
            route = Route.from_dict(data)
            route_lst.append(route)

        return route_lst
    
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

        data_lst = res["response"]["body"]["items"]["item"]
        station_lst = [] 
        for data in data_lst: # 이거 값이 하나일 때랑 여러개일 때 파일이 다름 하나일 땐 dict, list[dict] 이렇게 되서 이거 고치면 될듯
            print(data)
            route = Station.from_dict(data)
            station_lst.append(route)

        return station_lst
    

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

        data = res["response"]["body"]["items"]["item"]
        route = Route.from_dict(data)

        return route

