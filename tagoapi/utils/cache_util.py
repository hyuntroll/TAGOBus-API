from typing import TYPE_CHECKING
from .cache import Cache
from ..models.BaseList import BaseList

if TYPE_CHECKING:
    from tagoapi.models import BaseModel


cache = Cache()   

# method에서만 사용할 함수
def covert_model(ttl: int = 86400, model: type["BaseModel"] = None, is_list: bool = True): # 데코레이터가 사용할 매개변수
    def decorator(fn): # 호출할 함수를 매개변수로 받음
        def inner(self, *args, **kwargs): # 호출할 함수의 매개변수를 받아서 이를 실행
            is_cached = kwargs.pop("_is_cached", True)

            key = _make_cache_key(*args, _fname=fn.__name__, **kwargs) if is_cached else None
            cached = cache.get(key) if key else None


            if cached is None:
                raw = fn(self, *args, **kwargs)
                if key:
                    cache.save(key, raw, ttl)
            else:
                raw = cached

            if model:
                ## convert list
                if isinstance(raw, list):
                    res = model.from_list(cached)
                else:
                    res = model.from_dict(cached)
                res.set_client(self)

                return res if is_list and not isinstance(res, BaseList) else BaseList(res)


            return raw
        return inner
    return decorator

def _make_cache_key(*args, _fname: str, **kwargs) -> str:
    return _fname + ":" + "&".join([str(a) for a in args]) + "&".join(
        f"{key}={value}" for key, value in kwargs.items()
    ) ## str로 나타낼 수 없으면 다르게 표시하도록