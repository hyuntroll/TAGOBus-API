import unittest
from unittest.mock import patch
from tagoapi import TAGOClient, TAGOAuth, cache

class TestTagoClient(unittest.TestCase):
    def setUp(self):
        self.client = TAGOClient(auth=TAGOAuth("dummy_api_key"))

    @patch.object(TAGOClient, "_get")
    def test_get_station_return_models(self, mock_get):
        # _get이 반환할 가짜 객체 생성
        fake_response = {
            "response": {
                "body": {
                    "items": {
                        "item":[
                            {'gpslati': 35.86615, 'gpslong': 128.60002, 'nodeid': 'DGB7001009400', 'nodenm': '삼덕교회',
                             'nodeno': 20075},
                            {'gpslati': 35.86615, 'gpslong': 128.60002, 'nodeid': 'DGB7001009400', 'nodenm': '삼덕교회',
                             'nodeno': 20075}
                        ]
                    }
                }
            }
        }
        mock_get.return_value = fake_response

        # 실행
        stations = self.client.get_station(cityCode=25, nodeNm="엄랭")


        print(stations)

    @patch.object(TAGOClient, "_get")
    def test_get_station_with_dict(self, mock_get):
        fake_response = { "response": { "body": {
            "items": {
                "item": {'gpslati': 35.86615, 'gpslong': 128.60002, 'nodeid': 'DGB7001009400', 'nodenm': '삼덕교회',
                             'nodeno': 20075}
            }
        }}}
        mock_get.return_value = fake_response

        stations = self.client.get_station(cityCode=543, nodeNm="엄랭1")

        print(cache.current_cache)
        print(stations)

    @patch.object(TAGOClient, "_get")
    def test_get_station_no_cache(self, mock_get):
        fake_response = {"response": {"body": {
            "items": {
                "item": {'gpslati': 35.86615, 'gpslong': 128.60002, 'nodeid': 'DGB1234123423', 'nodenm': '이거보세요!!',
                         'nodeno': 20075}
            }
        }}}
        mock_get.return_value = fake_response

        stations = self.client.get_station_by_gps(gpsLati=1, gpsLong=3.425)

        print(stations)

    @patch.object(TAGOClient, "_get")
    def test_get_station_once(self, mock_get):
        fake_response = {"response": {"body": {
            "items": {
                "item": {'routeid': "DGB573493541", 'routeno': 356, 'routetp': '123', 'nodenm': '이거보세요!!',
                         'nodeno': 20075}
            }
        }}}
        mock_get.return_value = fake_response

        route = self.client.get_route_by_id(cityCode=25, routeId="DGB573493541")

        print(route._client)


if __name__ == "__main__":
    unittest.main()