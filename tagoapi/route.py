from .client import TAGOClient
from .auth import TAGOAuth
from .utils import *



class BusRoute(TAGOClient):
    SERVICE_URL = "BusRouteInfoInqireService"
    
    def __init__(self, auth: TAGOAuth):
        super().__init__(auth) 

    # @from_cache_or_fetch(604800)
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


# 버스 노선 자체에 관한 정보
class Route:
    def __init__(self, data: dict):
        self.routeId = data.get("routeid")
        self.routeNo = data.get("routeno")
        self.routeTp = data.get("routetp")
        self.endnode = data.get("endnode") # 다른 곳에서 표시할 땐 이름으로
        self.startnode = data.get("startnode")
        self.endvhicletime = data.get("endvhicletime")
        self.startvehicletime = data.get("startvehicletime")

    def __repr__(self):
        return f"<Route {self.routeNo}>"

# 업데이트 
class Vehicle:
    def __init__(self, route: Route, data: dict):
        self.route = route 
        self.gpsLati = data.get("gpslati")
        self.gpsLong = data.get("gpslong")
        self.nodeOrd = data.get("nodeord")
        self.vehicleNo = data.get("vehicleno") # 다른 곳에서 표시할 때 이 이름도 함께
    
    def __repr__(self):
        return f"<Route {self.route.routeNo} - {self.vehicleNo}>"
