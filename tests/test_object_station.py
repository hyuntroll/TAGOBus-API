import copy
import unittest
from unittest.mock import MagicMock

from src.tagoapi.models import Route, Station

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.station = Station("DGB573493541", "대구소프트웨어마이스터고등학교앞")
    def test_attributes(self): ## 속성 테스트
        print("\n====== test attributes ======")

        print("station:", self.station)

    def test_AttributeError(self): ## 없는 속성 테스트
        print("\n====== test AttributeError ======")

        with self.assertRaises(AttributeError):
            print("name:", self.station.name)

    def test_RuntimeError(self): ## client 주입 테스트
        print("\n====== test RuntimeError ======")

        with self.assertRaises(RuntimeError):
            print("endtime:", self.station.routes)

    def test_lazy_loading_station(self):
        print("\n====== test lazy_loading_station ( attribute not in class ======")

        station = copy.deepcopy(self.station)

        mock_client = MagicMock()
        mock_client._get_routes_by_station.return_value = [
            Route("564", city_code=22, route_no="북구2"),
            Route("564", city_code=22, route_no="북구2"),
            Route("564", city_code=22, route_no="북구2"),
        ]
        station.bind_client(mock_client)

        print(station.routes)

if __name__ == '__main__':
    unittest.main()
