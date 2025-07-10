from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = TAGOClient(auth=TAGOAuth(api_key))

lst = client.get_route_by_no(cityCode=22, routeNo="순환")
pprint([i.to_dict() for i in lst])

test_dict = client.get_route_by_id(22, routeId="DGB3000653000")
pprint(test_dict.to_dict())

lst_st = client.get_routes_by_stations(22, "DGB7001009400")
pprint([i.to_dict() for i in lst_st])


# def get_route_list():
#     global client
#     res = client._get_route_by_routeNo(cityCode=22, routeNo="북구")
#     return res
# def get_stations_by_route():
#     global client
#     res = client.get_stations_by_route(cityCode=22, routeId='DGB3000653000')
#     return res
# def get_route_info():
#     global client
#     res = client._get_route_info(cityCode=22, routeId='DGB3000653000')
#     return res

# if __name__ == "__main__":
    # pprint(get_route_list())
    # pprint(get_stations_by_route())
    # pprint(get_route_info())

    # pprint(client._get_route_by_routeNo.__code__.co_varnames)

    # route = client.get_route(22, routeId="DGB3000653000")

    # pprint(route)
    # pprint(client.get_route(22, routeNo="3"))