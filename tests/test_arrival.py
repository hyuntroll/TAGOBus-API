from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
auth = TAGOAuth(api_key)
client = TAGOClient(auth)

def get_station_arrivals():
    global auth, client
    res = client.get_station_arrivals(cityCode=22, nodeId='DGB7021050800')
    return res
def get_station_route_arrival():
    global auth, client
    res = client.get_station_route_arrival(cityCode=22, nodeId='DGB7021050800', routeId='DGB3000653000')
    return res

def test_get_station_route_arrivals():
    assert(
        get_station_arrivals(), dict
    )
def test_get_station_route_arrival():
    assert(
        get_station_route_arrival(), dict
    )




if __name__ == "__main__":
    pprint(get_station_arrivals())
    pprint(get_station_route_arrival())
