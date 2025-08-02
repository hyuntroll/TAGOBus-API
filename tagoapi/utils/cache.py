import os, pickle
from time import time

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = 'caches/cache.pkl' 

class Cache:
    def __init__(self, path: str = CACHE_PATH):
        self.path = os.path.join(MODULE_DIR, "....", path)
        self.path = os.path.abspath(self.path)
        os.makedirs("caches", exist_ok=True)

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
    
    @property
    def current_cache(self):
        return self._cache

