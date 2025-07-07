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

def prepare_params(
        auth: TAGOAuth, 
        params: dict, 
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


