import unittest
from unittest.mock import MagicMock

from src.tagoapi.models import Route, Station

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.route = Route("453", city_code=22, route_no="북구1")
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
            print("endtime:", self.route.end_vehicle_time)

    def test_lazy_load_in_class(self): ## lazy_load ( attribute in class )
        print("\n====== test lazy_load ( attribute in class ) ======")

        route = Route("453", city_code=22, route_no="북구4")

        # client_mock 생성
        mock_client = MagicMock()
        mock_client._get_route.return_value = Route(
            "453",
            city_code=22,
            route_no="북구4",
            end_vehicle_time=53,
        )
        route.bind_client(mock_client)

        print(route.route_no)

        print(route.end_vehicle_time)

    def test_custom_lazy_load_not_in_class(self): ## custom lazy_load ( attribute not in class )
        print("\n====== test custom lazy_load ( attribute not in class ) ======")

        class CustomRoute(Route):
            _lazy_fields = {
                **Route._lazy_fields,
                "stations": "get_stations",
            }

        route = CustomRoute("564", city_code=22, route_no="북구2")

        mock_client = MagicMock()
        mock_client.get_stations.return_value = [
            Station("안녕하시귀", "이런다"),
            Station("안녕하시귀", "이런다1"),
            Station("안녕하시귀", "이런다2"),
            Station("안녕하시귀", "이런다3")
        ]

        route.bind_client(mock_client)

        print(route.route_no)
        print(route.stations)

    def test_lazy_load_not_in_class(self): ## lazy_load ( attribute not in class )
        print("\n====== test lazy_load ( attribute not in class ) ======")

        route = Route("564", city_code=22, route_no="북구2")

        mock_client = MagicMock()
        mock_client._get_stations_by_route.return_value = [
            Station("안녕하시귀", "이런다"),
            Station("안녕하시귀", "이런다1"),
            Station("안녕하시귀", "이런다2"),
            Station("안녕하시귀", "이런다3")
        ]

        route.bind_client(mock_client)

        print(route.route_no)
        print(route.stations[0]._client)



if __name__ == '__main__':
    unittest.main()
