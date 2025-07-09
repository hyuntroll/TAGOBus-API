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
    
    @from_cache_or_fetch(86400)
    def get_station(
        self,
        cityCode: int,
        nodeId: str = '',
        nodeNm: str = '',
        nodeNo: str = None
    ) -> Union[list[Station], Station]:
        
        return None

    def get_station_arrivals(
        self,
        cityCode: int,
        nodeId: str,
    ) -> list[Vehicle]:
        endpoint = f'{self.AVRINFO}/getSttnAcctoArvlPrearngeInfoList'
        res = self._get(endpoint=endpoint, params={"cityCode": cityCode, "nodeId": nodeId})
        if res["totalCount"] == 0:
            return []
        vc_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
        return Vehicle.from_list(vc_list)
    
    def get_station_route_arrival(
        self,
        cityCode: int,
        nodeId: str,
        routeId: str,
    ) -> list[Vehicle]:
        endpoint = f'{self.AVRINFO}/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
        res = self._get(endpoint=endpoint, params={"cityCode": cityCode,"nodeId": nodeId,"routeId": routeId,})
        if res["totalCount"] == 0:
            return []
        vc_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
        return Vehicle.from_list(vc_list)
    

    @from_cache_or_fetch(604800)
    def get_route_by_no(
        self,
        cityCode: int,
        routeNo: str
    ) -> list[Route]:
        endpoint = f'{self.BUSROUTE}/getRouteNoList'
        params = build_params(self.auth, cityCode=cityCode, routeNo=routeNo)
        res = parse_metadata(self._get1(endpoint, params=params))
        if res is None:
            return None
        if isinstance(res, list):
            return convert(res, Route.from_list)
        else:
            return convert([res], Route.from_list)
        
    @from_cache_or_fetch(604800)
    def get_route_by_id(
        self,
        cityCode: int,
        routeId: str
    ) -> Route:
        endpoint = f'{self.BUSROUTE}/getRouteInfoIem'
        params = build_params(self.auth, cityCode=cityCode, routeId=routeId)
        res = parse_metadata(self._get1(endpoint, params=params))
        if res is None:
            return None
        
        return convert(res, Route.from_dict)



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


    # def _get(self, endpoint: str, params: dict) -> dict:
    #     response = requests.get(f"{self.BASE_URL}/{endpoint}", 
    #         params=prepare_params(self.auth, params))
        
    #     response.raise_for_status()
    #     striped_data = parse_metadata(response.json())

    #     return striped_data
    
    def _get1(self, endpoint: str, params: dict) -> any:
        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        # 모두 추출하지 못한 경우 -> 더 추출해야함
        return response.json()

    def _generate_route(self, res: dict) -> Union[list[Route], Route]:
        totalCount = res.get("totalCount", None)
        item = res.get("item", None)
        if not totalCount and not item: # 총 개수랑 item이 없을 경우
            return None
        elif not totalCount and item: # 아이템이 하나인 경우
            return Route.from_dict(item)
        else:
            return Route.from_list(item) # 아이템이 여러개인 경우





# def _generate_route(self, res: dict) -> Union[list[Route], Route]:
#     count = res.get("totalCount", None)
#     if count == 0 or res.get("items").get("item"):
#         return []
#     elif count == None:
#         pass
#     route_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
#     return Route.from_list(route_list)


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


# @overload
# def get_route(self, cityCode: int, routeNo: str) -> Union[list[Route], Route]: ...
# @overload
# def get_route(self, cityCode: int, routeId: str) -> Route: ...

# @from_cache_or_fetch(604800)
# def get_route(
#     self,
#     cityCode: int,
#     routeNo: Optional[str] = None,
#     routeId: Optional[str] = None
# ) -> Union[list[Route], Route]:
#     if routeNo and routeId:
#         raise ValueError("Only one of 'routeId' or 'routeNo' should be provided.")
#     if routeNo:
#         return self._get_route_by_routeNo(cityCode, routeNo)
#     elif routeId:
#         return self._get_route_info(cityCode, routeId)
#     else:
#         raise ValueError("At least one argument must be non-None.")

#     # return self._get1(endpoint, cityCode=cityCode, routeNo=routeNo, routeId=routeId)
#     # return self._generate_route(self._get1(endpoint, cityCode=cityCode, routeNo=routeNo, routeId=routeId))