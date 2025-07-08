from .client import TAGOClient
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
        # print(res["response"]["body"]["items"])
        route_lst = [] 
        for key, data in res["response"]["body"]["items"].items(): # 이거 값이 하나일 때랑 여러개일 때 파일이 다름 하나일 땐 dict, list[dict] 이렇게 되서 이거 고치면 될듯
            # print(data, type(data))
            route = Route(data)
            route_lst.append(route)

        return route_lst
    

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

