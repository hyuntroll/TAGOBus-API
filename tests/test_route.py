from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
auth = TAGOAuth(api_key)
client = TAGOClient(auth)

def get_route_list():
    global auth, client
    res = client.get_route_list(22, 6)
    return res
def get_stations_by_route():
    global auth, client
    res = client.get_stations_by_route(cityCode=22, routeId='DGB3000653000')
    return res
def get_route_info():
    global auth,client
    res = client.get_route_info(cityCode=22, routeId='DGB3000653000')
    return res

def test_get_route_list():
    assert(
        get_route_list(), dict
    )
def test_get_stations_by_route():
    assert(
        get_stations_by_route(), dict
    )
def test_get_route_info():
    assert(
        get_route_info(), dict
    )

if __name__ == "__main__":
    # pprint(get_route_list())
    # pprint(get_stations_by_route())
    pprint(get_route_info())
