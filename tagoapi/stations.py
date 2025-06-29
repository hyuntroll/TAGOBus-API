from tagoapi.client import TAGOClient

def get_station_by_keyword( client: TAGOClient, cityCode: int, keyword: str ) -> dict:
    endpoint = "BusSttnInfoInqireService/getSttnNoList"
    params = { "cityCode": cityCode, "nodeNm": keyword, "_type": "json"}
    return client.get(endpoint=endpoint, params=params)
