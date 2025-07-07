from .client import TAGOClient
from .auth import TAGOAuth
from .utils import *


class BusPosition(TAGOClient):
    SERVICE_URL = "BusLcInfoInqireService"
    
    def __init__(self, auth: TAGOAuth):
        super().__init__(auth) 

    def get_route_pos(
        self, 
        cityCode: int,
        routeId: int,
    ) -> dict:
            
        endpoint = f'{self.SERVICE_URL}/getRouteAcctoBusLcList'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeId": routeId,
            }
        ) 

        res = self.get(endpoint=endpoint, params=params)
        return res

    def get_route_pos_near_station(
        self, 
        cityCode: int,
        routeId: int,
        nodeId: int,
    ) -> dict:
            
        endpoint = f'{self.SERVICE_URL}/getRouteAcctoSpcifySttnAccesBusLcInfo'
        params = prepare_params(
            self.auth,
            {
                "cityCode": cityCode,
                "routeId": routeId,
                "nodeId": nodeId
            }
        ) 

        res = self.get(endpoint=endpoint, params=params)
        return res
