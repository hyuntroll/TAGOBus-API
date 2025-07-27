from tagoapi import *
from dotenv import load_dotenv
import os
from pprint import pprint
import time

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = TAGOClient(auth=TAGOAuth(api_key))


start = time.time()
gps_lst = client.get_station_by_gps(35.86613, 128.600068)
end = time.time()
print(gps_lst)
print(f"{end - start:.5f}")

start = time.time()
st_lst = client.get_station_by_route(22, "DGB3000653000")
end = time.time()
print(st_lst)
print(f"{end - start:.5f}")

start = time.time()
test_ = client.get_station(22, nodeNm="민들레아파트후문건너")
end = time.time()
print(test_)
print(f"{end - start:.5f}")




# def get_station_info_by_name():
#     global client
#     res = client.get_station_info_by_name(cityCode=22, nodeNm='대구소프트웨어')
#     return res
# def get_station_info_by_gps():
#     global client
#     res = client.get_station_info_by_gps(cityCode=22, gpsLati=35.91650, gpsLong= 128.62907)
#     return res
# def get_routes_by_stations():
#     global client
#     res = client.get_routes_by_stations(cityCode=22, nodeId='DGB7021050700')
#     return res

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

# if __name__ == "__main__":
#     pprint(get_station_info_by_name())
#     pprint(get_station_info_by_gps())
#     pprint(get_routes_by_stations())
#     # pprint(get_city_code())

#     for station in get_station_info_by_gps():
#         print(station.to_dict())
