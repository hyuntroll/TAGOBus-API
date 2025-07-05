

class TAGOAuth:
    def __init__(self, serviceKey: str):
        if not isinstance(serviceKey, str):
            raise TypeError("Service key must be a string")
        
        self.serviceKey = serviceKey

    def getServiceKey(self):
        return self.serviceKey