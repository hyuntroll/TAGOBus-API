import pandas as pd, os
from tagoapi.models import Station
from .cache import Cache

# def csv_to_dict(csvfile, encoding):
#     loaded_csv = pd.read_csv(csvfile, encoding=encoding)
#     data = loaded_csv.to_dict(orient='records')
#     return data
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(MODULE_DIR, ".."))
CACHE_DIR = os.path.join(PROJECT_ROOT, "caches")
STATION_CACHE_PATH = os.path.join(CACHE_DIR, "station.pkl")
cache = Cache(STATION_CACHE_PATH)
station_list = cache.get("stations_2025_06_15.csv")

def get_station(keyword) -> list[Station]:
    result = []
    for station in station_list:
        if  keyword in station["정류장명"]:
            result.append(
                Station.from_dict({
                    "nodeid": station["정류장번호"],
                    "nodenm": station["정류장명"],
                    "nodeno": station["모바일단축번호"],
                    "gpslati": station["위도"],
                    "gpslong": station["경도"],
                    "citycode": station["도시코드"]
                })
            )
    

    return station_list


# if not station_list:
#     station_list = csv_to_dict("tagoapi/csv/stations_2025_06_15.csv", 'cp949')
#     cache.save("stations_2025_06_15.csv", station_list)

