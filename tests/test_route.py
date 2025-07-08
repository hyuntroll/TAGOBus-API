from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = BusRoute(auth=TAGOAuth(api_key))

def get_route_list():
    global client
    res = client.get_route_list(cityCode=22, routeNo="순환")
    return res
def get_stations_by_route():
    global client
    res = client.get_stations_by_route(cityCode=22, routeId='DGB3000653000')
    return res
def get_route_info():
    global client
    res = client.get_route_info(cityCode=22, routeId='DGB2000002000')
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
    pprint(get_stations_by_route())
    pprint(get_route_info())

    lst = get_route_list()

    for route in lst:
        print(route.to_dict())
