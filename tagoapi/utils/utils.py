# def get_city_code(serviceKey) -> dict:
#     # 요청 후에 캐시로 저장하는 코드
#     key = "BusSttnInfoInqireService/getCtyCodeList"
#     cached = cache.get(key)
#     if cached:
#         print("cache hit!")
#         return cached
    
#     print("cache miss!")
#     path = "http://apis.data.go.kr/1613000/BusSttnInfoInqireService/getCtyCodeList"
#     params = {'_type': 'json', "serviceKey": serviceKey}
#     res = requests.get(path, params=params).json()

#     cache.save(key, res, 15552000)
#     return res