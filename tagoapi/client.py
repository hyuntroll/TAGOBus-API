from .exceptions import *
from .utils.decorator import *
from .utils import *
from .models import *

from typing import Optional, overload



class TAGOClient:
    BASE_URL = "http://apis.data.go.kr/1613000"
    AVRINFO = "ArvlInfoInqireService"
    BUSROUTE = 'BusRouteInfoInqireService'
    BUSTATION = "BusSttnInfoInqireService"
    BUSPOS = "BusLcInfoInqireService"
    CACHE_TTL = 604800


    def __init__(self, service_key: str):
        self.service_key = service_key

    @overload
    def get_station(self, city_code: int, station_no: int) -> list[Station]: ...
    @overload
    def get_station(self, city_code: int, station_no: Optional[int], station_name: str) -> list[Station]: ...

    @convert_model(604800, Route)
    def get_route_by_no(
        self,
        city_code: int = None,
        route_no: str = None,
        cityCode: int = None,
        routeNo: str = None,
    ) -> list[Route]:
        """노선 번호로 버스를 조회합니다
        :param city_code: 도시 코드
        :param route_no: 노선 번호
        """
        city_code = city_code if city_code is not None else cityCode
        route_no = route_no if route_no is not None else routeNo
        endpoint = f'{self.BUSROUTE}/getRouteNoList'
        params = build_params(self.service_key, kwargs={"city_code": city_code, "route_no": route_no})
        return self._fetch_and_convert(endpoint, params, city_code=city_code)
        
    @convert_model(604800, Route, is_list=False)
    def get_route_by_id(
        self,
        city_code: int = None,
        route_id: str = None,
        cityCode: int = None,
        routeId: str = None,
    ) -> Route:
        """노선 ID로 버스 정보를 조회합니다"""
        city_code = city_code if city_code is not None else cityCode
        route_id = route_id if route_id is not None else routeId
        endpoint = f'{self.BUSROUTE}/getRouteInfoIem'
        params = build_params(self.service_key, kwargs={"city_code": city_code, "route_id": route_id})
        return self._fetch_and_convert(endpoint, params, city_code=city_code)

    @convert_model(604800, Route)
    def get_route_by_station(
        self,
        city_code: int = None,
        station_id: str = None,
        cityCode: int = None,
        nodeId: str = None,
    ) -> list[Route]:
        """정류소를 경유하는 노선을 조회합니다"""
        city_code = city_code if city_code is not None else cityCode
        station_id = station_id if station_id is not None else nodeId
        endpoint = f'{self.BUSTATION}/getSttnThrghRouteList'
        params = build_params(self.service_key, kwargs={"city_code": city_code, "station_id": station_id})
        return self._fetch_and_convert(endpoint, params, city_code=city_code)
    

    @convert_model(604800, Station)
    def get_station_by_route(
        self,
        city_code: int = None,
        route_id: str = None,
        cityCode: int = None,
        routeId: str = None,
    ) -> list[Station]:
        """노선이 경유하는 정류소를 조회합니다"""
        city_code = city_code if city_code is not None else cityCode
        route_id = route_id if route_id is not None else routeId
        endpoint = f'{self.BUSROUTE}/getRouteAcctoThrghSttnList'
        params = build_params(self.service_key, kwargs={"city_code": city_code, "route_id": route_id})
        return self._fetch_and_convert(endpoint, params, city_code=city_code)
    
    @convert_model(86400, Station)
    def get_station(
        self,
        city_code: int = None,
        station_no: int = None,
        station_name: str = None,
        cityCode: int = None,
        nodeNo: int = None,
        nodeNm: str = None,
    ) -> list[Station]:
        """정류소명 또는 번호로 정류소를 조회합니다"""
        city_code = city_code if city_code is not None else cityCode
        station_no = station_no if station_no is not None else nodeNo
        station_name = station_name if station_name is not None else nodeNm
        if not (station_no or station_name):
            raise ValueError("Only one of 'station_no' or 'station_name' should be provided.")

        endpoint = f'{self.BUSTATION}/getSttnNoList'
        params = build_params(self.service_key, kwargs={"city_code": city_code, "station_no": station_no, "station_name": station_name})
        return self._fetch_and_convert(endpoint, params, city_code=city_code)
    
    @convert_model(86400, Station, is_cached=False)
    def get_station_by_gps(
        self,
        gps_lati: float = None,
        gps_long: float = None,
        gpsLati: float = None,
        gpsLong: float = None,
    ) -> list[Station]:
        """GPS 좌표 기반으로 주변 정류소를 조회합니다"""
        gps_lati = gps_lati if gps_lati is not None else gpsLati
        gps_long = gps_long if gps_long is not None else gpsLong
        endpoint = f'{self.BUSTATION}/getCrdntPrxmtSttnList'
        params = build_params(self.service_key, kwargs={"gps_lati": gps_lati, "gps_long": gps_long})
        return self._fetch_and_convert(endpoint, params)

    @convert_model(model=ArrivalInfo, is_cached=False)
    def get_arrival_by_station(
        self,
        city_code: int = None,
        station_id: str = None,
        node_id: str = None,
        cityCode: int = None,
        nodeId: str = None,
    ) -> list[ArrivalInfo]:
        """실시간 도착예정정보 및 운행정보 목록을 조회합니다"""
        city_code = city_code if city_code is not None else cityCode
        normalized_station_id = station_id or node_id or nodeId
        endpoint = f'{self.AVRINFO}/getSttnAcctoArvlPrearngeInfoList'
        params = build_params(self.service_key, kwargs={"city_code": city_code, "nodeId": normalized_station_id})
        return self._fetch_and_convert(endpoint, params, city_code=city_code)

    @convert_model(model=ArrivalInfo, is_cached=False)
    def get_route_arrival_by_station(
        self,
        city_code: int = None,
        station_id: str = None,
        node_id: str = None,
        route_id: str = None,
        cityCode: int = None,
        nodeId: str = None,
        routeId: str = None,
    ) -> list[ArrivalInfo]:
        """특정노선의 실시간 도착예정정보 및 운행정보 목록을 조회합니다"""
        city_code = city_code if city_code is not None else cityCode
        normalized_station_id = station_id or node_id or nodeId
        normalized_route_id = route_id or routeId
        endpoint = f'{self.AVRINFO}/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
        params = build_params(
            self.service_key,
            kwargs={"city_code": city_code, "nodeId": normalized_station_id, "routeId": normalized_route_id},
        )
        return self._fetch_and_convert(endpoint, params, city_code=city_code)
    
    @convert_model(model=Vehicle, is_cached=False)
    def get_route_pos(
        self, 
        city_code: int = None,
        route_id: int = None,
        cityCode: int = None,
        routeId: int = None,
    ) -> list[Vehicle]:
        """버스의 S위치정보의 목록을 조회합니다"""
        city_code = city_code if city_code is not None else cityCode
        normalized_route_id = route_id if route_id is not None else routeId
        endpoint = f'{self.BUSPOS}/getRouteAcctoBusLcList'
        params = build_params(self.service_key, kwargs={"city_code": city_code, "routeId": normalized_route_id})
        return self._fetch_and_convert(endpoint, params, city_code=city_code)

    @convert_model(model=Vehicle, is_cached=False)
    def get_route_pos_near_station(
        self, 
        city_code: int = None,
        route_id: int = None,
        station_id: int = None,
        node_id: int = None,
        cityCode: int = None,
        routeId: int = None,
        nodeId: int = None,
    ) -> list[Vehicle]:
        """특정정류소에 접근한 버스의 위치정보를 조회합니다"""
        city_code = city_code if city_code is not None else cityCode
        normalized_route_id = route_id if route_id is not None else routeId
        normalized_station_id = (
            station_id
            if station_id is not None
            else (node_id if node_id is not None else nodeId)
        )
        endpoint = f'{self.BUSPOS}/getRouteAcctoSpcifySttnAccesBusLcInfo'
        params = build_params(
            self.service_key,
            kwargs={"city_code": city_code, "routeId": normalized_route_id, "nodeId": normalized_station_id},
        )
        return self._fetch_and_convert(endpoint, params, city_code=city_code)


    ######## method for LazyLoading ################


    def _get_route(self, route: Route) -> Route:
        return self.get_route_by_id(route.city_code, route.route_id)

    def _get_stations_by_route(self, route: Route) -> list[Station]:
        return self.get_station_by_route(route.city_code, route.route_id)

    def _get_station(self, station: Station) -> Station:
        return self.get_station(station.city_code, station_name=station.station_name)[0]

    def _get_routes_by_station(self, station: Station) -> list[Route]:
        return self.get_route_by_station(station.city_code, station.station_id)

    def _get_station_by_arrival_info(self, arrival_info: ArrivalInfo) -> Station:
        return self.get_station(arrival_info.city_code, station_no=arrival_info.station_no)[0]

    def _get_route_by_arrival_info(self, arrival_info: ArrivalInfo) -> Route:
        return self.get_route_by_id(arrival_info.city_code, arrival_info.route_id)

    def _get_route_by_vehicle(self, vehicle: Vehicle) -> Route:
        return self.get_route_by_id(vehicle.city_code, vehicle.route_id)

    def _get_station_by_vehicle(self, vehicle: Vehicle) -> Station:
        return self.get_station(vehicle.city_code, station_no=vehicle.station_no)[0];

    ######## get util ################


    def _fetch_and_convert(
            self,
            endpoint: str,
            params: dict,
            city_code: int,
            **kwargs
    ) -> list | dict:
        response = parse_metadata(self._get(endpoint, params))
        return {"result":response, "city_code": city_code}

    def _get(self, endpoint: str, params: dict) -> any:
        response = http_get(f"{self.BASE_URL}/{endpoint}", params=params)
        error_code = response.get("returnReasonCode")

        if not error_code:
            return response
        
        if error_code == '20':
            raise ServiceAccessDeniedError("서비스에 접근이 거부되었습니다.")
        elif error_code == '22':
            raise RequestExcessdsError("서비스 요청제한횟수를 초과했습니다.")
        elif error_code == '30':
            raise ServiceKeyNotRegisteredError("유효하지 않는 서비스키 입니다.")
        elif error_code == '31':
            raise DeadLineHasExpired("API활용기간이 만료되었습니다.")
        elif error_code == '32':
            raise UnRegisteredIpError("등록되지 않은 IP입니다.")
        else:
            raise RuntimeError(f"실행중 오류가 발생했습니다. 에러코드: {error_code}")
