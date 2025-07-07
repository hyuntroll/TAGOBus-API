from .client import TAGOClient
from .auth import TAGOAuth
from .utils import *


class BusStation(TAGOClient):
    SERVICE_URL = "BusSttnInfoInqireService"
    
    def __init__(self, auth: TAGOAuth):
        super().__init__(auth) 
    
    def get_station_info_by_name(
        self,
        cityCode: int,
        nodeNm: str = '',
        nodeNo: str = '',
        endpoint: str = f'{SERVICE_URL}/getSttnNoList'
    ) -> dict:
        
        params = {
                "cityCode": cityCode,
                "nodeNm": nodeNm,
                "nodeNo": nodeNo,
            }
        

        params = prepare_params(self.auth, params)
        res = self.get(endpoint=endpoint, params=params)
        return res
    
    def get_station_info_by_gps(
        self,
        cityCode: int,
        gpsLati: int,
        gpsLong: int,
        endpoint: int = f'{SERVICE_URL}/getCrdntPrxmtSttnList'
    ) -> dict:
        
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "gpsLati": gpsLati,
                "gpsLong": gpsLong,
            }
        )

        res = self.get(endpoint=endpoint, params=params)
        return res
    
    def get_routes_by_stations(
        self,
        cityCode: int,
        nodeId: str,
        endpoint: str = f'{SERVICE_URL}/getSttnThrghRouteList'
    ) -> dict:
        
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "nodeid": nodeId,
            }
        )

        res = self.get(endpoint=endpoint, params=params)
        return res
    