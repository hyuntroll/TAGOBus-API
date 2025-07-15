

class TAGOAuth:
    def __init__(self, serviceKey: str):
        if not isinstance(serviceKey, str):
            raise TypeError("Service key must be a string")
        
        self._serviceKey = serviceKey

    @property
    def serviceKey(self):
        return self._serviceKey