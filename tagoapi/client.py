from .exceptions import *
from .utils import *
from .models import *
from .auth import TAGOAuth

from typing import Union, Optional, overload



class TAGOClient:
    BASE_URL = "http://apis.data.go.kr/1613000"
    AVRINFO = "ArvlInfoInqireService"
    BUSROUTE = 'BusRouteInfoInqireService'
    BUSTATION = "BusSttnInfoInqireService"
    BUSPOS = "BusLcInfoInqireService"
    CACHE_TTL = 604800


    def __init__(self, auth: TAGOAuth):
        if not isinstance(auth, TAGOAuth):
            raise TypeError("Expected 'auth' to be an instance of TAGOAuth")
        
        self.auth = auth

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
        return self._fetch_and_convert(endpoint, params, Route)
        
    @from_cache_or_fetch(604800)
    def get_route_by_id(
        self,
        cityCode: int,
        routeId: str
    ) -> Route:
        endpoint = f'{self.BUSROUTE}/getRouteInfoIem'
        params = build_params(self.auth, cityCode=cityCode, routeId=routeId)
        return self._fetch_and_convert(endpoint, params, Route, is_list=False)

    @from_cache_or_fetch()
    def get_route_by_station(
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
    ) -> list[Station]:
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
        if not (nodeNo or nodeNm):
            raise ValueError("Only one of 'nodeNo' or 'nodeNm' should be provided.")

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


    def get_arrival_by_station(
        self,
        cityCode: int,
        nodeId: str,
    ) -> list[ArrivalInfo]:
        endpoint = f'{self.AVRINFO}/getSttnAcctoArvlPrearngeInfoList'
        params = build_params(self.auth, cityCode=cityCode, nodeId=nodeId)
        return self._fetch_and_convert(endpoint, params, ArrivalInfo)
    
    def get_route_arrival_by_station(
        self,
        cityCode: int,
        nodeId: str,
        routeId: str,
    ) -> list[ArrivalInfo]:
        endpoint = f'{self.AVRINFO}/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
        params = build_params(self.auth, cityCode=cityCode, nodeId=nodeId, routeId=routeId)
        return self._fetch_and_convert(endpoint, params, ArrivalInfo)
    

    def get_route_pos(
        self, 
        cityCode: int,
        routeId: int,
    ) -> list[Vehicle]:
        endpoint = f'{self.BUSPOS}/getRouteAcctoBusLcList'
        params = build_params(self.auth, cityCode=cityCode, routeId=routeId)
        return self._fetch_and_convert(endpoint, params, Vehicle, is_cache=False)

    def get_route_pos_near_station(
        self, 
        cityCode: int,
        routeId: int,
        nodeId: int,
    ) -> list[Vehicle]:
        endpoint = f'{self.BUSPOS}/getRouteAcctoSpcifySttnAccesBusLcInfo'
        params = build_params(self.auth, cityCode=cityCode, routeId=routeId, nodeId=nodeId)
        return self._fetch_and_convert(endpoint, params, Vehicle)



    def _fetch_and_convert(
            self, 
            endpoint: str, 
            params: dict, 
            model: BaseModel,
            is_list: bool = True,
            is_cache: bool = True
    ) -> BaseModel:
        cache_key = KeyExtract(model)
        response = parse_metadata(self._get(endpoint, params))
        if not response: 
            return None 
        if isinstance(response, list):
            if not is_cache:
                return convert(response, model.from_list)
            result = []
            for v in response:
                key = cache_key.generate_key(v)
                cached = cache.get(key)
                if cached:
                    result.append(cached)
                else:
                    parsed_obj = convert(v, model.from_dict)
                    result.append(parsed_obj)
                    cache.save(key, parsed_obj, self.CACHE_TTL)

            return result

        else:
            if is_cache: 
                key = cache_key.generate_key(response)
                cached = cache.get(key)
                if cached:
                    return [cached] if is_list else cached
            result = convert(response, model.from_dict)
            cache.save(key, result, self.CACHE_TTL)
            return [result] if is_list else result

    
    def _get(self, endpoint: str, params: dict) -> any:
        response = http_get(f"{self.BASE_URL}/{endpoint}", params=params)
        error_code = response.get("returnReasonCode")
        if error_code == '30':
            raise ServiceKeyNotRegisteredError("유효하지 않는 서비스키 입니다.")
        elif error_code:
            raise RuntimeError(f"실행중 오류가 발생했습니다. 에러코드: {error_code}")

        return response