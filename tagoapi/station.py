from .client import TAGOClient
from .utils import *
from .models import *

class BusStation(TAGOClient):
    SERVICE_URL = "BusSttnInfoInqireService"
    
    def __init__(self, auth: TAGOAuth):
        super().__init__(auth) 
    
    @from_cache_or_fetch(86400)
    def get_station_info_by_name(
        self,
        cityCode: int,
        nodeNm: str = '',
        nodeNo: str = ''
    ) -> list[Station]:
        endpoint = f'{self.SERVICE_URL}/getSttnNoList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "nodeNm": nodeNm,
                "nodeNo": nodeNo,
            }
        )
        res = self.get(endpoint=endpoint, params=params)
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
        endpoint = f'{self.SERVICE_URL}/getCrdntPrxmtSttnList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "gpsLati": gpsLati,
                "gpsLong": gpsLong,
            }
        )
        res = self.get(endpoint=endpoint, params=params)

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
        
        endpoint = f'{self.SERVICE_URL}/getSttnThrghRouteList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "nodeid": nodeId,
            }
        )

        res = self.get(endpoint=endpoint, params=params)
        if res["totalCount"] == 0:
            return []
        route_list = res["items"]["item"] if isinstance(res["items"]["item"], list) else [res["items"]["item"]]
        return Route.from_list(route_list)
    