from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = TAGOClient(auth=TAGOAuth(api_key))

def get_route_list():
    global client
    res = client.get_route_list(cityCode=22, routeNo="북구4")
    return res
def get_stations_by_route():
    global client
    res = client.get_stations_by_route(cityCode=22, routeId='DGB3000653000')
    return res
def get_route_info():
    global client
    res = client.get_route_info(cityCode=22, routeId='DGB2000002000')
    return res



if __name__ == "__main__":
    pprint(get_route_list())
    pprint(get_stations_by_route())
    pprint(get_route_info())

    # lst = get_route_list()


    # 이제 사용 X
    # for route in lst:
    #     print(route.to_dict())
