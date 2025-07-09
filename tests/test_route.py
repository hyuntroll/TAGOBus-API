from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = TAGOClient(auth=TAGOAuth(api_key))

def get_route_list():
    global client
    res = client._get_route_by_routeNo(cityCode=22, routeNo="북구")
    return res
def get_stations_by_route():
    global client
    res = client.get_stations_by_route(cityCode=22, routeId='DGB3000653000')
    return res
def get_route_info():
    global client
    res = client._get_route_info(cityCode=22, routeId='')
    return res



if __name__ == "__main__":
    # pprint(get_route_list())
    # pprint(get_stations_by_route())
    # pprint(get_route_info())

    # route = client.get_route(22, routeId="DGB3000653000")

    # pprint(route)
    pprint(client.get_route(22, routeNo="북구4"))