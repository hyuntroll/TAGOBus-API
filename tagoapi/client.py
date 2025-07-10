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
    def get_station(self, cityCode: int, nodeNo: int) -> list[Station]: ...
    @overload
    def get_station(self, cityCode: int, nodeNo: Optional[int], nodeNm: str) -> list[Station]: ...

    @from_cache_or_fetch(604800)
    def get_route_by_no(
        self,
        cityCode: int,
        routeNo: str
    ) -> list[Route]:
        endpoint = f'{self.BUSROUTE}/getRouteNoList'
        params = build_params(self.auth, cityCode=cityCode, routeNo=routeNo)
        return self._fetch_and_convert(endpoint, params,Route)
        
    @from_cache_or_fetch(604800)
    def get_route_by_id(
        self,
        cityCode: int,
        routeId: str
    ) -> Route:
        endpoint = f'{self.BUSROUTE}/getRouteInfoIem'
        params = build_params(self.auth, cityCode=cityCode, routeId=routeId)
        return self._fetch_and_convert(endpoint, params, Route)

    @from_cache_or_fetch()
    def get_routes_by_stations(
        self,
        cityCode: int,
        nodeId: str
    ) -> list[Route]:
        endpoint = f'{self.BUSTATION}/getSttnThrghRouteList'
        params = build_params(self.auth, cityCode=cityCode, nodeId=nodeId)
        return self._fetch_and_convert(endpoint, params, Route)
    

    @from_cache_or_fetch(604800)
    def get_station_by_route(
        self,
        cityCode: int,
        routeId: str
    ) -> list[Route]:
        endpoint = f'{self.BUSROUTE}/getRouteAcctoThrghSttnList'
        params= build_params(self.auth, cityCode=cityCode, routeId=routeId)
        return self._fetch_and_convert(endpoint, params, Station)
    
    @from_cache_or_fetch(86400)
    def get_station(
        self,
        cityCode: int,
        nodeNo: int = None,
        nodeNm: str = None,
    ) -> list[Station]:
        endpoint = f'{self.BUSTATION}/getSttnNoList'
        params= build_params(self.auth, cityCode=cityCode, nodeNm=nodeNm,nodeNo=nodeNo)
        return self._fetch_and_convert(endpoint, params, Station)
    
    @from_cache_or_fetch(86400)
    def get_station_by_gps(
        self,
        gpsLati: float,
        gpsLong: float
    ) -> list[Station]:
        endpoint = f'{self.BUSTATION}/getCrdntPrxmtSttnList'
        params = build_params(self.auth, gpsLati=gpsLati, gpsLong=gpsLong)
        return self._fetch_and_convert(endpoint, params, Station)


    def get_station_arrivals(
        self,
        cityCode: int,
        nodeId: str,
    ) -> list[Vehicle]:
        endpoint = f'{self.AVRINFO}/getSttnAcctoArvlPrearngeInfoList'
        params = build_params(self.auth, cityCode=cityCode, nodeId=nodeId)
        return self._fetch_and_convert(endpoint, params, Vehicle)
    
    def get_station_route_arrival(
        self,
        cityCode: int,
        nodeId: str,
        routeId: str,
    ) -> list[Vehicle]:
        endpoint = f'{self.AVRINFO}/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
        params = build_params(self.auth, cityCode=cityCode, nodeId=nodeId, routeId=routeId)
        return self._fetch_and_convert(endpoint, params, Vehicle)
    

    def get_route_pos(
        self, 
        cityCode: int,
        routeId: int,
    ) -> list[Vehicle]:
        endpoint = f'{self.BUSPOS}/getRouteAcctoBusLcList'
        params = build_params(self.auth, cityCode=cityCode, routeId=routeId)
        return self._fetch_and_convert(endpoint, params, Vehicle)

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
    def _fetch_and_convert(
            self, 
            endpoint: str, 
            params: dict, 
            model,
            is_list: bool = True
        ) -> U:
            res = parse_metadata(self._get(endpoint, params))
            if not res: 
                return None 
            if isinstance(res, list): 
                return convert(res, model.from_list) 
            else: 
                return convert([res], model.from_list) if is_list else convert(res,  model.from_dict) 
    
    def _get(self, endpoint: str, params: dict) -> any:
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

#     # return self._get(endpoint, cityCode=cityCode, routeNo=routeNo, routeId=routeId)
#     # return self._generate_route(self._get(endpoint, cityCode=cityCode, routeNo=routeNo, routeId=routeId))