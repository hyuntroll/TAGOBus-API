import unittest
from unittest.mock import MagicMock

from tagoapi.models import Route, Station
from tagoapi.models.BaseList import BaseList

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

    # def test_lazy_load_not_in_class(self): ## lazy_load ( attribute not in class )
    #     print("\n====== test lazy_load ( attribute not in class ) ======")
    #
    #
    #     station = Station("DGB573493541", "대구소프트웨어마이스터고등학교앞")
    #
    #     # client_mock 생성
    #     mock_client = MagicMock()
    #     mock_client._get_station.return_value = Station("DGB573493541", "대구소프트웨어마이스터고등학교앞")
    #     station.set_client(mock_client)
    #
    #     print(station.nodeNm)
    #
    #     print(station.station)



if __name__ == '__main__':
    unittest.main()