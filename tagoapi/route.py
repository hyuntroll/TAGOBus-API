from tagoapi.client import TAGOClient


def get_city_code( client: TAGOClient ) -> dict:
    if not isinstance(client, TAGOClient):
        raise TypeError("Expected 'client' to be an instance of TAGOClient ")
    endpoint = "ArvlInfoInqireService/getCtyCodeList"
    params = { "_type": "json" }
    return client.get(endpoint=endpoint, params=params)
