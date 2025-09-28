import unittest
from unittest.mock import patch
from tagoapi import TAGOClient, TAGOAuth
from tagoapi.models import Station

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


        print(stations[0]._client)


if __name__ == "__main__":
    unittest.main()