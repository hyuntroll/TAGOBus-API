from .exceptions import *
from .utils import *
from typing import Union, Optional, overload


class TAGOClient:
    BASE_URL = "http://apis.data.go.kr/1613000"
    AVRINFO = "ArvlInfoInqireService"
    BUSROUTE = 'BusRouteInfoInqireService'
    BUSTATION = "BusSttnInfoInqireService"
    BUSPOS = "BusLcInfoInqireService"


    def __init__(self, auth: TAGOAuth):
        if not isinstance(auth, TAGOAuth):
            raise TypeError("Expected 'auth' to be an instance of TAGOAuth")
        
        self.auth = auth

        # self._cache = Cache()
    @overload
    def get_route(self, cityCode: int, routeNo: str) -> Union[list[Route], Route]: ...
    @overload
    def get_route(self, cityCode: int, routeId: str) -> Route: ...

    def _get(self, endpoint: str, params: dict) -> dict:
        response = requests.get(f"{self.BASE_URL}/{endpoint}", 
            params=prepare_params(self.auth, params))
        
        response.raise_for_status()
        striped_data = strip_meta(response.json())

        return striped_data

    @from_cache_or_fetch(604800)
    def get_route(
        self,
        cityCode: int,
        routeNo: Optional[str] = None,
        routeId: Optional[str] = None
    ) -> Union[list[Route], Route]:
        if not routeNo and not routeId:
            raise ValueError("At least one argument must be non-None.")
        elif routeNo and routeId:
            raise ValueError("Only one of 'routeId' or 'routeNo' should be provided.")

    def get_station_arrivals(
        self,
        cityCode: int,
        nodeId: str,
    ) -> dict:
        endpoint = f'{self.AVRINFO}/getSttnAcctoArvlPrearngeInfoList'

        res = self._get(endpoint=endpoint, params={"cityCode": cityCode, "nodeId": nodeId})
        return res
    
    def get_station_route_arrival(
        self,
        cityCode: int,
        nodeId: str,
        routeId: str,
    ) -> dict:
        
        endpoint = f'{self.AVRINFO}/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "nodeId": nodeId,
                "routeId": routeId,
            }
        )

        res = self._get(endpoint=endpoint, params=params)
        return res


    @from_cache_or_fetch(604800)
    def get_route_list(
        self,
        cityCode: int,
        routeNo: int
    ) -> list[Route]:
        endpoint = f'{self.BUSROUTE}/getRouteNoList'
        res = self._get(endpoint, params={"cityCode": cityCode,"routeNo": routeNo})
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
        endpoint = f'{self.BUSROUTE}/getRouteAcctoThrghSttnList'
        res = self._get(endpoint, params={"cityCode": cityCode, "routeId": routeId})
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
        endpoint = f'{self.BUSROUTE}/getRouteInfoIem'
        res = self._get(endpoint, params={"cityCode": cityCode, "routeId": routeId})

        if not res["items"]["item"]:
            return None
        route = Route.from_dict(res["items"]["item"])

        return route


    @from_cache_or_fetch(86400)
    def get_station_info_by_name(
        self,
        cityCode: int,
        nodeNm: str = '',
        nodeNo: str = ''
    ) -> list[Station]:
        endpoint = f'{self.BUSTATION}/getSttnNoList'
        res = self._get(endpoint=endpoint, params={"cityCode": cityCode,"nodeNm": nodeNm,"nodeNo": nodeNo})
        if res["totalCount"] == 0:
            return []
        
        station_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
        return Station.from_list(station_list)
    
    @from_cache_or_fetch()
    def get_station_info_by_gps(
        self,
        cityCode: int,
        gpsLati: int,
        gpsLong: int
    ) -> list[Station]:
        endpoint = f'{self.BUSTATION}/getCrdntPrxmtSttnList'
        res = self._get(endpoint=endpoint, params={"cityCode": cityCode,"gpsLati": gpsLati,"gpsLong": gpsLong})


        if res["totalCount"] == 0:
            return []
        
        station_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
        return Station.from_list(station_list)
    
    @from_cache_or_fetch()
    def get_routes_by_stations(
        self,
        cityCode: int,
        nodeId: str
    ) -> list[Route]:
        endpoint = f'{self.BUSTATION}/getSttnThrghRouteList'
        res = self._get(endpoint=endpoint, params={"cityCode": cityCode, "nodeId": nodeId})

        if res["totalCount"] == 0:
            return []
        route_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
        return Route.from_list(route_list)
    

    def get_route_pos(
        self, 
        cityCode: int,
        routeId: int,
    ) -> dict:
        endpoint = f'{self.BUSPOS}/getRouteAcctoBusLcList'
        res = self._get(endpoint=endpoint, params={"cityCode": cityCode, "routeId": routeId})
        return res

    def get_route_pos_near_station(
        self, 
        cityCode: int,
        routeId: int,
        nodeId: int,
    ) -> dict:
        endpoint = f'{self.BUSPOS}/getRouteAcctoSpcifySttnAccesBusLcInfo'
        res = self._get(endpoint=endpoint, params={"cityCode": cityCode, "routeId": routeId, "nodeId": nodeId})
        return res





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
