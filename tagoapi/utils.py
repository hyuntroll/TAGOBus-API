from .auth import TAGOAuth
from .models import *
from .cache import Cache
from typing import Union, Callable, TypeVar, Any
import requests
import os
from time import time

T = TypeVar('T', dict, list) # list, dict으로 매개변수 받을 때
U = TypeVar('U', dict[str], list) # list, dict으로 반환할 때

CACHE_PATH = 'caches/cache.pkl' 
cache = Cache()

class KeyExtract:
    def __init__(self, model: BaseModel):
        self.model = model
        self.raw_key = model.cache_key
        self._args = self._check_bracket(self.raw_key)

    @property
    def key_args(self):
        return self._args
    
    def generate_key(self, **kwargs: dict) -> str:
        generated_key = self.raw_key
        if len(kwargs) > len(self._args):
            raise TypeError(f"generate_key() takes {len(self._args)} positional argument but {len(kwargs)} were given")
        
        #TODO: 이거 self._args말고 kwargs.keys해서 arg랑 대응 시켜서 없으면 raise 이런식으로 작성해도 좋을 듯
        for arg in self._args:
            k = kwargs.get(arg, None)
            if not k:
                raise TypeError()
            generated_key = generated_key.replace(f"<{arg}>", k)

        return generated_key


            

    def _check_bracket(self, data: str) -> list:
        args = []
        current_match = None
        fa = ''
        for w in data:
            if current_match:
                fa += w

            if w == '<':
                current_match = True
            elif w == '>':
                if not current_match:
                    return None # 에러를 나타내든 뭐를 하든 
                current_match = False
                args.append(fa[:-1].strip()); fa = ''

        return args

            
            






    

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

def parse_metadata(res: dict) -> U:
    striped = res.get("response", {}).get("body", {}).get("items", {})
    if isinstance(striped, dict):
        return striped.get("item", None)

    return None

def convert(res: T, converter: Callable[[T], U]) -> U:
    if not res:
        return None
    return converter(res)

def build_params(
        auth: TAGOAuth,  
        numOfRows: int = 10, 
        pageNo: int = 1,
        **kwargs: dict
    ) -> dict:

    return {
        "serviceKey": auth.getServiceKey(),
        "numOfRows": numOfRows,
        "pageNo": pageNo,
        "_type": "json",
        **{key: value for key, value in kwargs.items() if value}
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

