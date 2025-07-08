from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = TAGOClient( auth=TAGOAuth(api_key) )


def get_station_arrivals():
    global client
    res = client.get_station_arrivals(cityCode=22, nodeId='DGB7021050800')
    return res
def get_station_route_arrival():
    global client
    res = client.get_station_route_arrival(cityCode=22, nodeId='DGB7021050800', routeId='DGB3000653000')
    return res

if __name__ == "__main__":

    # print(client.get_route(22, routeId="DGB3000653000", routeNo="adf"))
    pprint(get_station_arrivals())
    pprint(get_station_route_arrival())
