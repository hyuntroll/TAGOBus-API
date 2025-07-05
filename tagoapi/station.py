from .client import TAGOClient
from .auth import TAGOAuth
from .utils import prepare_params


class BusStation(TAGOClient):
    SERVICE_URL = "BusSttnInfoInqireService"
    
    def __init__(self, auth: TAGOAuth):
        super().__init__(auth) 
    
    def get_station_info_by_name(
        self,
        cityCode: int,
        nodeNm: str = '',
        nodeNo: str = '',
        numOfRows: int = 10, 
        pageNo: int = 1
    ) -> dict:
        
        endpoint = f'{self.SERVICE_URL}/getSttnNoList'
        params = prepare_params (
            self.auth,
            {
                "cityCode": cityCode,
                "nodeNm": nodeNm,
                "nodeNo": nodeNo,
            }
        )

        res = self.get(endpoint=endpoint, params=params)
        return res
    
    def get_station_info_by_gps(
        self,
        cityCode: int,
        gpsLati: int,
        gpsLong: int,
    ) -> dict:
        
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
        return res
    
    def get_routes_by_stations(
        self,
        cityCode: int,
        nodeId: str,
        numOfRows: int = 10, 
        pageNo: int = 1
    ) -> dict:
        
        endpoint = f'{self.SERVICE_URL}/getSttnThrghRouteList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "nodeid": nodeId,
            }
        )

        res = self.get(endpoint=endpoint, params=params)
        return res
    