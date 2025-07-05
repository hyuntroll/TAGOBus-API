from .exceptions import *
import requests
from .auth import TAGOAuth


class TAGOClient:
    BASE_URL = "http://apis.data.go.kr/1613000"

    def __init__(self, auth: TAGOAuth):
        """
        summery
        """
        if not isinstance(auth, TAGOAuth):
            raise TypeError("Expected 'client' to be an instance of TAGOClient ")
        
        self.auth = auth

    def get(self, endpoint: str, params: dict) -> dict:
        params = self.auth.apply(params)

        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
    

        return response.json()
    

    def get_route_list(
            self, 
            cityCode: int,
            routeNo: int,
            numOfRows: int = 10, 
            pageNo: int = 1
        ) -> dict:
            
            endpoint = 'BusRouteInfoInqireService/getRouteNoList'
            params = {
                      "cityCode": cityCode,
                      "routeNo": routeNo,
                      "numOfRows": numOfRows,
                      "pageNo": pageNo,
                      "_type": 'json'
                 }

            res = self.get(endpoint=endpoint, params=params)
            return res
    
    def get_stations_by_route(
            self,
            cityCode: int,
            routeId: str,
            numOfRows: int = 10, 
            pageNo: int = 1
        ) -> dict:
        
            endpoint = 'BusRouteInfoInqireService/getRouteAcctoThrghSttnList'
            params = {
                    "cityCode": cityCode,
                    "routeId": routeId,
                    "numOfRows": numOfRows,
                    "pageNo": pageNo,
                    "_type": 'json'
                }

            res = self.get(endpoint=endpoint, params=params)
            return res
    
    def get_route_info(
            self,
            cityCode: int,
            routeId: str,
        ) -> dict:
            
            endpoint = 'BusRouteInfoInqireService/getRouteInfoIem'
            params = {
                    "cityCode": cityCode,
                    "routeId": routeId,
                    "_type": 'json'
                }

            res = self.get(endpoint=endpoint, params=params)
            return res
    
    def get_station_arrivals(
            self,
            cityCode: int,
            nodeId: str,
            numOfRows: int = 10, 
            pageNo: int = 1
        ) -> dict:
        
            endpoint = 'ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList'
            params = {
                    "cityCode": cityCode,
                    "nodeId": nodeId,
                    "numOfRows": numOfRows,
                    "pageNo": pageNo,
                    "_type": 'json'
                }

            res = self.get(endpoint=endpoint, params=params)
            return res
    
    def get_station_route_arrival(
            self,
            cityCode: int,
            nodeId: str,
            routeId: str,
            numOfRows: int = 10, 
            pageNo: int = 1
        ) -> dict:
        
            endpoint = 'ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
            params = {
                    "cityCode": cityCode,
                    "nodeId": nodeId,
                    "routeId": routeId,
                    "numOfRows": numOfRows,
                    "pageNo": pageNo,
                    "_type": 'json'
                }

            res = self.get(endpoint=endpoint, params=params)
            return res
    
    def get_station_info_by_name(
            self,
            cityCode: int,
            nodeNm: str = '',
            nodeNo: str = '',
            numOfRows: int = 10, 
            pageNo: int = 1
        ) -> dict:
        
            endpoint = 'BusSttnInfoInqireService/getSttnNoList'
            params = {
                    "cityCode": cityCode,
                    "nodeNm": nodeNm,
                    "nodeNo": nodeNo,
                    "numOfRows": numOfRows,
                    "pageNo": pageNo,
                    "_type": 'json'
                }

            res = self.get(endpoint=endpoint, params=params)
            return res
    
    def get_station_info_by_gps(
            self,
            cityCode: int,
            gpsLati: int,
            gpsLong: int,
            numOfRows: int = 10, 
            pageNo: int = 1
        ) -> dict:
        
            endpoint = 'BusSttnInfoInqireService/getCrdntPrxmtSttnList'
            params = {
                    "cityCode": cityCode,
                    "gpsLati": gpsLati,
                    "gpsLong": gpsLong,
                    "numOfRows": numOfRows,
                    "pageNo": pageNo,
                    "_type": 'json'
                }

            res = self.get(endpoint=endpoint, params=params)
            return res
    
    def get_routes_by_stations(
            self,
            cityCode: int,
            nodeId: str,
            numOfRows: int = 10, 
            pageNo: int = 1
        ) -> dict:
        
            endpoint = 'BusSttnInfoInqireService/getSttnThrghRouteList'
            params = {
                    "cityCode": cityCode,
                    "nodeid": nodeId,
                    "numOfRows": numOfRows,
                    "pageNo": pageNo,
                    "_type": 'json'
                }

            res = self.get(endpoint=endpoint, params=params)
            return res
    
