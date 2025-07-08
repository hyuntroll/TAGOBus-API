from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = BusStation(auth=TAGOAuth(api_key))


def get_station_info_by_name():
    global client
    res = client.get_station_info_by_name(cityCode=22, nodeNm='대구소프트웨어')
    return res
def get_station_info_by_gps():
    global client
    res = client.get_station_info_by_gps(cityCode=22, gpsLati=35.91650, gpsLong= 128.62907)
    return res
def get_routes_by_stations():
    global client
    res = client.get_routes_by_stations(cityCode=22, nodeId='DGB7021050700')
    return res


# def test_get_station_info_by_name():
#     assert(
#         get_station_info_by_name(), dict
#     )
# def test_get_station_info_by_gps():
#     assert(
#         get_station_info_by_gps(), dict
#     )
# def test_get_routes_by_stations():
#     assert(
#         get_routes_by_stations(), dict
#     )

if __name__ == "__main__":
    pprint(get_station_info_by_name())
    pprint(get_station_info_by_gps())
    pprint(get_routes_by_stations())
    # pprint(get_city_code())

    for station in get_station_info_by_gps():
        print(station.to_dict())
