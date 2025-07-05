from .auth import TAGOAuth
import requests

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

def get_city_code() -> dict:
    # 요청 후에 캐시로 저장하는 코드
    
    path = "http://apis.data.go.kr/1613000/BusSttnInfoInqireService/getCtyCodeList"
    params = {'_type': 'json'}
    res = requests(endpoint=path, params=params)
    return res
