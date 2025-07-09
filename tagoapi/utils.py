from .auth import TAGOAuth
from .models import *
from .cache import Cache
from typing import Union
import requests
import os
from time import time

CACHE_PATH = 'caches/cache.pkl' 
cache = Cache()

# method에서만 사용할 함수
def from_cache_or_fetch(ttl: int = 86400): # 데코레이터가 사용할 매개변수
    def real_deco(fn): # 호출할 함수를 매개변수로 받음
        def wrapper(self, *args, **kwargs): # 호출할 함수의 매개변수를 받아서 이를 실행
            key = generate_cache_key(*args, _fname=fn.__name__, **kwargs)
            cached = cache.get(key)
            if cached:
                return cached
            
            result = fn(self, *args, **kwargs)
            cache.save(key, result, ttl)
            return result

        return wrapper
    
    return real_deco

def generate_cache_key(*args, _fname: str, **kwargs) -> str:
    return _fname + ":" + "&".join([str(a) for a in args]) + "&".join(
        f"{key}={value}" for key, value in kwargs.items()
    ) ## str로 나타낼 수 없으면 다르게 표시하도록


    # return endpoint + "?" + "&".join(
    #             f"{key}={value}" for key, value in kwargs.items()
    #         )

def parse_metadata(res: dict) -> dict | list:
    striped = res.get("response", {}).get("body", {}).get("items", {})
    if isinstance(striped, dict):
        return striped.get("item", None)

    return None


def prepare_params(
        auth: TAGOAuth, 
        params: dict = dict(), 
        numOfRows: int = 10, 
        pageNo: int = 1
    ) -> dict:

    return {
        **params,
        "serviceKey": auth.getServiceKey(),
        "numOfRows": numOfRows,
        "pageNo": pageNo,
        "_type": "json"
        }

def get_city_code(serviceKey) -> dict:
    # 요청 후에 캐시로 저장하는 코드
    key = "BusSttnInfoInqireService/getCtyCodeList"
    cached = cache.get(key)
    if cached:
        print("cache hit!")
        return cached
    
    print("cache miss!")
    path = "http://apis.data.go.kr/1613000/BusSttnInfoInqireService/getCtyCodeList"
    params = {'_type': 'json', "serviceKey": serviceKey}
    res = requests.get(path, params=params).json()

    cache.save(key, res, 15552000)
    return res

