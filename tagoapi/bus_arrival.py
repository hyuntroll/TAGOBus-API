from .client import TAGOClient
from .utils import *


class BusArrival(TAGOClient):
    SERVICE_URL = "ArvlInfoInqireService"
    
    def __init__(self, auth: TAGOAuth):
        super().__init__(auth)

    def get_station_arrivals(
        self,
        cityCode: int,
        nodeId: str,
    ) -> dict:
        
        endpoint = f'{self.SERVICE_URL}/getSttnAcctoArvlPrearngeInfoList'
        params = prepare_params(
            self.auth, 
            {
                "cityCode": cityCode,
                "nodeId": nodeId,
            }
        )

        res = self.get(endpoint=endpoint, params=params)
        return res
    
    def get_station_route_arrival(
        self,
        cityCode: int,
        nodeId: str,
        routeId: str,
    ) -> dict:
        
        endpoint = f'{self.SERVICE_URL}/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "nodeId": nodeId,
                "routeId": routeId,
            }
        )

        res = self.get(endpoint=endpoint, params=params)
        return res
