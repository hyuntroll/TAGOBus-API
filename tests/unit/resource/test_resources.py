from tagoapi.models import ArrivalInfo, Route, Station, Vehicle
from tagoapi.resources import (
    ArrivalResource,
    RouteResource,
    StationResource,
    VehicleResource,
)


class FakeTransport:
    def __init__(self, item):
        self.calls: list[dict] = []
        self.response = {
            "response": {
                "header": {
                    "resultCode": "00",
                    "resultMsg": "NORMAL SERVICE",
                },
                "body": {
                    "items": {"item": item},
                    "pageNo": 1,
                    "numOfRows": 10,
                    "totalCount": 1,
                },
            }
        }

    def request(self, path: str, *, params: dict) -> dict:
        self.calls.append({"path": path, "params": params})
        return self.response


def test_route_resource_maps_route_and_station_endpoints():
    route_transport = FakeTransport({
        "routeid": "R1",
        "routeno": "100",
        "routetp": "간선버스",
        "startvehicletime": "0600",
    })
    routes = RouteResource(route_transport)

    route_page = routes.list(25, "100")
    route = route_page.items[0]

    assert isinstance(route, Route)
    assert route.city_code == 25
    assert route.start_vehicle_time == "0600"
    assert route_transport.calls[0] == {
        "path": "/BusRouteInfoInqireService/getRouteNoList",
        "params": {
            "pageNo": 1,
            "numOfRows": 10,
            "cityCode": 25,
            "routeNo": "100",
            "_type": "json",
        },
    }

    station_transport = FakeTransport({
        "routeid": "R1",
        "nodeid": "N1",
        "nodenm": "중앙역",
        "nodeord": 3,
    })
    station = RouteResource(station_transport).list_stations(25, "R1").items[0]
    assert isinstance(station, Station)
    assert station.city_code == 25


def test_route_resource_get_maps_single_and_empty_responses():
    transport = FakeTransport({
        "routeid": "R1",
        "routeno": "100",
        "startvehicletime": 600,
    })
    resource = RouteResource(transport)

    route = resource.get(25, "R1")

    assert route is not None
    assert route.start_vehicle_time == "0600"
    assert transport.calls[0] == {
        "path": "/BusRouteInfoInqireService/getRouteInfoIem",
        "params": {
            "cityCode": 25,
            "routeId": "R1",
            "_type": "json",
        },
    }

    transport.response["response"]["body"]["items"] = {}
    assert resource.get(25, "R1") is None


def test_station_resource_uses_documented_parameter_casing():
    transport = FakeTransport({
        "routeid": "R1",
        "routeno": "100",
        "routetp": "간선버스",
        "startnodenm": "기점",
        "endnodenm": "종점",
    })

    route = StationResource(transport).list_routes(25, "N1").items[0]

    assert isinstance(route, Route)
    assert transport.calls[0]["params"]["nodeid"] == "N1"
    assert "nodeId" not in transport.calls[0]["params"]


def test_station_search_and_nearby_use_exact_documented_keys():
    search_transport = FakeTransport({
        "nodeid": "N1",
        "nodenm": "중앙역",
        "nodeno": 1001,
    })
    station = StationResource(search_transport).list(
        25,
        station_name="중앙역",
        station_no="1001",
    ).items[0]

    assert station.station_no == "1001"
    assert search_transport.calls[0]["params"] == {
        "pageNo": 1,
        "numOfRows": 10,
        "cityCode": 25,
        "nodeNm": "중앙역",
        "nodeNo": "1001",
        "_type": "json",
    }

    nearby_transport = FakeTransport({
        "nodeid": "N2",
        "nodenm": "인근역",
        "citycode": "25",
        "gpslati": "36.1",
        "gpslong": "127.1",
    })
    nearby = StationResource(nearby_transport).list_nearby(
        36.1,
        127.1,
    ).items[0]

    assert nearby.city_code == 25
    assert nearby_transport.calls[0]["params"]["gpsLati"] == 36.1
    assert nearby_transport.calls[0]["params"]["gpsLong"] == 127.1


def test_arrival_resource_injects_request_context():
    transport = FakeTransport({
        "nodenm": "중앙역",
        "routeid": "R1",
        "routeno": "100",
        "routetp": "간선버스",
        "arrprevstationcnt": 2,
        "vehicletp": "일반",
        "arrtime": 180,
    })

    arrival = ArrivalResource(transport).list_by_station(25, "N1").items[0]

    assert isinstance(arrival, ArrivalInfo)
    assert arrival.city_code == 25
    assert arrival.station_id == "N1"
    assert arrival.station_name == "중앙역"


def test_arrival_resource_maps_station_and_route_endpoint():
    transport = FakeTransport({
        "nodenm": "중앙역",
        "routeno": "100",
        "routetp": "간선버스",
        "arrprevstationcnt": "2",
        "vehicletp": "일반",
        "arrtime": "180",
    })

    arrival = ArrivalResource(transport).list_by_station_and_route(
        25,
        "N1",
        "R1",
    ).items[0]

    assert arrival.route_id == "R1"
    assert arrival.station_id == "N1"
    assert transport.calls[0]["path"].endswith(
        "/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"
    )
    assert transport.calls[0]["params"]["routeId"] == "R1"


def test_vehicle_resource_fills_fields_missing_from_response():
    transport = FakeTransport({
        "routenm": "202",
        "gpslati": "36.333445",
        "gpslong": "127.438859",
        "nodeid": "N1",
        "nodenm": "중앙역",
        "nodeord": 1,
        "routetp": "간선버스",
        "vehicleno": "대전99가9999",
    })

    vehicle = VehicleResource(transport).list_by_route(25, "R1").items[0]

    assert isinstance(vehicle, Vehicle)
    assert vehicle.route_id == "R1"
    assert vehicle.city_code == 25
    assert vehicle.route_no == "202"
    assert vehicle.station_id == "N1"
    assert vehicle.node_order == 1


def test_vehicle_approaching_station_injects_route_and_station_ids():
    transport = FakeTransport({
        "routenm": "102",
        "nodenm": "중앙역",
        "routetp": "간선버스",
        "gpslati": "36.3",
        "gpslong": "127.4",
    })

    vehicle = VehicleResource(transport).list_approaching_station(
        25,
        "R1",
        "N1",
    ).items[0]

    assert vehicle.route_id == "R1"
    assert vehicle.station_id == "N1"
    assert transport.calls[0]["path"].endswith(
        "/getRouteAcctoSpcifySttnAccesBusLcInfo"
    )
    assert transport.calls[0]["params"]["nodeId"] == "N1"
