from unittest import result

from .cache import Cache


cache = Cache()   

# method에서만 사용할 함수
def from_cache_or_fetch(ttl: int = 86400): # 데코레이터가 사용할 매개변수
    def real_deco(fn): # 호출할 함수를 매개변수로 받음
        def wrapper(self, *args, **kwargs): # 호출할 함수의 매개변수를 받아서 이를 실행

            model = kwargs.get('_model') or getattr(fn, '_model', None)
            is_list = kwargs.get('_is_list', True)

            if kwargs.get("_is_cache", True):
                key = generate_cache_key(*args, _fname=fn.__name__, **kwargs)
                cached = cache.get(key)

                # 만약 캐시가 없다면
                if not cached:
                    cached = fn(self, *args, **kwargs)
                    cache.save(key, cached, ttl)
            else:
                cached = fn(self, *args, **kwargs)

            ## convert list
            if isinstance(cached, list):
                res = model.from_list(cached)
                res.set_client(self)
                return res
            else:
                res = model.from_dict(cached)
                res.set_client(self)
                return res if not is_list else [res]


        return wrapper
    return real_deco

def generate_cache_key(*args, _fname: str, **kwargs) -> str:
    return _fname + ":" + "&".join([str(a) for a in args]) + "&".join(
        f"{key}={value}" for key, value in kwargs.items()
    ) ## str로 나타낼 수 없으면 다르게 표시하도록