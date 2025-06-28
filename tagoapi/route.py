from tagoapi.client import TAGOClient


def get_city_code( client: TAGOClient ) -> dict:
    endpoint = "ArvlInfoInqireService/getCtyCodeList"
    params = { "_type": "json"}
    return client.get(endpoint=endpoint, params=params)
