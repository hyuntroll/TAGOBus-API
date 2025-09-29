import unittest
from unittest.mock import MagicMock

from tagoapi.models import Route, Station
from tagoapi.models.BaseList import BaseList

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = Route("453", routeNo="북구1")
    def test_attributes(self): ## 속성 테스트
        print("\n====== test attributes ======")

        print("route:", self.route)

    def test_AttributeError(self): ## 없는 속성 테스트
        print("\n====== test AttributeError ======")

        with self.assertRaises(AttributeError):
            print("name:", self.route.name)

    def test_RuntimeError(self): ## client 주입 테스트
        print("\n====== test RuntimeError ======")

        with self.assertRaises(RuntimeError):
            print("endtime:", self.route.endvehicletime)

    def test_lazy_load_in_class(self): ## lazy_load ( attribute in class )
        print("\n====== test lazy_load ( attribute in class ) ======")

        route = Route("453", routeNo="북구4")

        # client_mock 생성
        mock_client = MagicMock()
        mock_client.get_route_by_id.return_value = Route("453", routeNo="북구4", endvehicletime=53)
        route.set_client(mock_client)

        print(route.routeNo)

        print(route.endvehicletime)

    def test_lazy_load_not_in_class(self): ## lazy_load ( attribute not in class )
        print("\n====== test lazy_load ( attribute not in class ) ======")

        route = Route("564", routeNo="북구2")

        mock_client = MagicMock()
        mock_client.get_stations.return_value = BaseList([
            Station("안녕하시귀", "이런다"),
            Station("안녕하시귀", "이런다1"),
            Station("안녕하시귀", "이런다2"),
            Station("안녕하시귀", "이런다3")
        ])

        route.set_client(mock_client)
        route._lazy_fields = {"stations": "get_stations"}

        print(route.routeNo)
        print(route.stations)




if __name__ == '__main__':
    unittest.main()