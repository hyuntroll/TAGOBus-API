import os, pickle
from time import time

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(MODULE_DIR, ".."))
CACHE_DIR = os.path.join(PROJECT_ROOT, "caches")
DEFAULT_CACHE_PATH = os.path.join(CACHE_DIR, "cache.pkl")


class Cache:
    """
        TTL 기반 캐시. 저장 값은 항상 dict/list[dict].
        도메인 객체는 캐시에서 꺼낼 때 변환 후 client 주입.
    """

    def __init__(self, path: str = DEFAULT_CACHE_PATH):
        self.path = os.path.abspath(path)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._cache = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            try:
                
                with open(self.path, 'rb') as f:
                    return pickle.load(f)
                
            except Exception as e:
                # print(e)
                return {}
        return {}

    def save(self, key: str, value: dict, ttl: int = 86400) -> bool:
        """
                value: dict 또는 list[dict]만 허용
        """
        if not isinstance(value, (dict, list)):
            raise TypeError("value must be a dict or list")
        self._cache[key] = {
            "value": value,
            "ttl": ttl,
            "saved_time": time()
        }
        self._dump()
        return True

    def get(self, key: str):
        entry = self._cache.get(key)
        if not entry:
            return None

        value, saved_time, ttl = entry["value"], entry["saved_time"], entry["ttl"]
        if time() - saved_time > ttl:
            del self._cache[key]
            return None
        return value

    def _dump(self):
        try:
            with open(self.path, "wb") as f:
                pickle.dump(self._cache, f)
        except Exception as e:
            print(f"[Cache] dump error: {e}")

    @property
    def current_cache(self):
        return self._cache
