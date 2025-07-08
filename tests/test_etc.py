from tagoapi import *
from pprint import pprint

# def get_inher():
#     auth = TAGOAuth(serviceKey='1234')
#     busRoute = BusRoute(auth)
#     return busRoute.test(), busRoute.test_url()

# def test_inher():
#     assert(get_inher(), ('1234', "http://apis.data.go.kr/1613000"))


if __name__ == "__main__":
    test_lst = [
        {'routeid': 'DGB2000002000', 'routeno': '순환2', 'routetp': '순환버스', 'endnode': None, 'startnode': None, 'endvehicletime': 2236, 'startvehicletime': 530},
        {'routeid': 'DGB2000002100', 'routeno': '순환2-1', 'routetp': '순환버스', 'endnode': None, 'startnode': None, 'endvehicletime': 2230, 'startvehicletime': 530},
        {'routeid': 'DGB2000003000', 'routeno': '순환3', 'routetp': '순환버스', 'endnode': None, 'startnode': None, 'endvehicletime': 2221, 'startvehicletime': 530},
        {'routeid': 'DGB2000003100', 'routeno': '순환3-1', 'routetp': '순환버스', 'endnode': None, 'startnode': None, 'endvehicletime': 2220, 'startvehicletime': 530}
    ]
    
    pprint(Route.from_list(test_lst))

    print(strip_meta(
        {"response": {
            "body": {
                "items": {
                    "item": [
                        {"a":1}, {"b":2}
                    ]
                }
            }
        }}
    ))