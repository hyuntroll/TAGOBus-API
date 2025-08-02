
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tagoapi import *
from tagoapi.utils.cache import Cache



def test_cache():
    cache = Cache("caches/station.pkl")
    station_list = cache.get("stations_2025_06_15.csv")
    assert isinstance(station_list, list)

def test_statin():
    assert isinstance(get_station("민들"), list)

