
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tagoapi import *
from tagoapi.utils.cache import Cache
import pprint



# def test_cache():
#     cache = Cache("caches/station.pkl")
#     station_list = cache.get("stations_2025_06_15.csv")
#     assert isinstance(station_list, list)

client = TAGOClient(TAGOAuth("xn4RVIhnt5Q5/+c7Z6EUFEMvixw/jR8fTaO9+rA+YqLawwW6Sv9e33bJhFDQWqjN+qo+Wxi6H6Qmzs8IAZdrBw=="))

# pprint.pprint(client.get_station(
#     25, nodeNo=44810, nodeNm="전통시장"
# ))

# pprint.pprint(client.get_station_by_gps(
#     gpsLati=36.3, gpsLong=127.3
# ))

pprint.pprint(client.get_route_by_station(
    22, "DGB7021050800"
))

##

# pprint.pprint(client.get_route_by_no(
#     25, routeNo=5
# ))

# pprint.pprint(client.get_station_by_route(
#     25, routeId="DJB30300004"
# ))

# pprint.pprint(client.get_route_by_id(
#     25, routeId="DJB30300004"
# ))

def test_statin():
    assert isinstance(get_station("민들"), list)

