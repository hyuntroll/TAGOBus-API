from .auth import TAGOAuth
import requests
import os, pickle
from time import time

CACHE_PATH = 'caches/cache.pkl'
class Cache:
    def __init__(self, path: str = CACHE_PATH):
        os.makedirs("caches", exist_ok=True)
        self.path = path
        self._cache = self._load()


    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def save(self, key: str, value: dict, ttl: int = 86400)  -> bool:
        os.makedirs("caches", exist_ok=True)
      
        self._cache[key] = {
            "value": value, 
            "ttl": ttl,
            "saved_time": time()
        }
        with open(self.path, 'wb') as f:
            pickle.dump(self._cache, f)
        
        return True
    
    def get(self, key: str) -> dict | bool:
        entry = self._cache.get(key)
        if not entry:
            return None
        

        value, saved_time, ttl = entry["value"], entry["saved_time"], entry["ttl"]
        
        if time() - saved_time > ttl:
            del self._cache[key]
            return None
        
        
        return value
cache = Cache()

# method에서만 사용할 함수
def from_cache_or_fetch(ttl: int = 86400): # 데코레이터가 사용할 매개변수
    def real_deco(fn): # 호출할 함수를 매개변수로 받음
        def wrapper(self, *args, **kwargs): # 호출할 함수의 매개변수를 받아서 이를 실행
            # print(kwargs, endpoint)
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
    # print(args, _fname, kwargs)
    return _fname + ":" + "&".join([a for a in args if a == int or a == str]) + "&".join(
        f"{key}={value}" for key, value in kwargs.items() if value == int or value == str
    )


    # return endpoint + "?" + "&".join(
    #             f"{key}={value}" for key, value in kwargs.items()
    #         )

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

