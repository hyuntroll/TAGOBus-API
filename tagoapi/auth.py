

class TAGOAuth:

    def __init__(self, serviceKey: str):
        """
        summery
        """
        if not isinstance(serviceKey, str):
            raise TypeError("Service key must be a string")
        self._serviceKey = serviceKey

        
        
    def apply(self, params: dict) -> dict: # 받은 params에 serviceKey를 붙여주는 방식
        new_params = params.copy() # 훼손 방지를 위해 깊은 복사
        new_params["serviceKey"] = self._serviceKey
        new_params["_type"] = 'json'
        return new_params
