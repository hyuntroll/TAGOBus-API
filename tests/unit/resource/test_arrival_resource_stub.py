import unittest

from src.tagoapi.resources.arrival_resource import ArrivalResource


class FakeHttpTransport:
    def __init__(self, response: dict):
        self.response = response
        self.calls = []

    def request(self, path: str, *, params: dict):
        self.calls.append({"path": path, "params": params})
        return self.response


class StubArrivalResource(ArrivalResource):
    def fetch_arrivals(self, city_code: int, node_id: str):
        return self._request(
            "/getSttnAcctoArvlPrearngeInfoList",
            {"cityCode": city_code, "nodeId": node_id},
        )


class TestArrivalResourceWithStubTransport(unittest.TestCase):
    def test_request_parses_single_item_as_dict(self):
        fake_response = {
            "response": {
                "body": {
                    "items": {
                        "item": {"nodeid": "N1", "nodenm": "테스트정류장"}
                    }
                }
            }
        }
        transport = FakeHttpTransport(fake_response)
        resource = StubArrivalResource(transport)

        result = resource.fetch_arrivals(city_code=25, node_id="N1")

        self.assertEqual({"nodeid": "N1", "nodenm": "테스트정류장"}, result)
        self.assertEqual(1, len(transport.calls))
        self.assertEqual(
            "/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList",
            transport.calls[0]["path"],
        )
        self.assertEqual(
            {"cityCode": 25, "nodeId": "N1", "_type": "json"},
            transport.calls[0]["params"],
        )

    def test_request_parses_multiple_items_as_list(self):
        fake_response = {
            "response": {
                "body": {
                    "items": {
                        "item": [
                            {"nodeid": "N1", "nodenm": "테스트정류장"},
                            {"nodeid": "N2", "nodenm": "테스트정류장2"},
                        ]
                    }
                }
            }
        }
        transport = FakeHttpTransport(fake_response)
        resource = StubArrivalResource(transport)

        result = resource.fetch_arrivals(city_code=25, node_id="N1")

        self.assertEqual(
            [
                {"nodeid": "N1", "nodenm": "테스트정류장"},
                {"nodeid": "N2", "nodenm": "테스트정류장2"},
            ],
            result,
        )
        self.assertEqual(1, len(transport.calls))
        self.assertEqual(
            "/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList",
            transport.calls[0]["path"],
        )
        self.assertEqual(
            {"cityCode": 25, "nodeId": "N1", "_type": "json"},
            transport.calls[0]["params"],
        )

    def test_request_returns_empty_dict_when_item_is_missing(self):
        fake_response = {
            "response": {
                "body": {
                    "items": {}
                }
            }
        }
        transport = FakeHttpTransport(fake_response)
        resource = StubArrivalResource(transport)

        result = resource.fetch_arrivals(city_code=25, node_id="N2")

        self.assertEqual({}, result)


if __name__ == "__main__":
    unittest.main()
