from unittest.mock import MagicMock

from tagoapi.models import ArrivalInfo, Route, Station, Vehicle


def test_route_maps_flat_payload_and_loads_detail_group_once():
    route = Route.from_dict({
        "routeid": "R1",
        "citycode": 22,
        "routeno": "100",
    })
    client = MagicMock()
    client._get_route.return_value = Route.from_dict({
        "routeid": "R1",
        "citycode": 22,
        "routeno": "100",
        "endvehicletime": 2330,
        "startvehicletime": 530,
    })
    route.bind_client(client)

    assert route.end_vehicle_time == "2330"
    assert route.start_vehicle_time == "0530"
    client._get_route.assert_called_once_with(route)


def test_station_allows_missing_coordinates_and_loads_details_once():
    station = Station.from_dict({
        "nodeid": "N1",
        "nodenm": "정류장",
        "citycode": 22,
    })
    client = MagicMock()
    client._get_station.return_value = Station.from_dict({
        "nodeid": "N1",
        "nodenm": "정류장",
        "citycode": 22,
        "nodeno": 1001,
        "gpslati": "35.1",
        "gpslong": 128.1,
    })
    station.bind_client(client)

    assert station.station_no == "1001"
    assert station.gps_latitude == 35.1
    assert station.gps_longitude == 128.1
    client._get_station.assert_called_once_with(station)


def test_arrival_maps_flat_payload_and_lazy_loads_relations():
    arrival = ArrivalInfo.from_dict({
        "nodeid": "N1",
        "routeid": "R1",
        "citycode": 22,
        "nodeno": 1001,
        "arrprevstationcnt": 2,
        "vehicletp": "일반",
        "arrtime": 180,
    })
    station = Station("N1", "정류장", city_code=22, station_no=1001)
    route = Route("R1", city_code=22, route_no="100")
    client = MagicMock()
    client._get_station_by_arrival_info.return_value = station
    client._get_route_by_arrival_info.return_value = route
    arrival.bind_client(client)

    assert arrival.station is station
    assert arrival.route is route
    assert arrival.previous_station_count == 2
    assert arrival.to_dict()["station"]["station_id"] == "N1"


def test_vehicle_maps_flat_payload_and_lazy_loads_relations():
    vehicle = Vehicle.from_dict({
        "routeid": "R1",
        "citycode": 22,
        "nodeno": 1001,
        "gpslati": "35.2",
        "gpslong": "128.2",
        "vehicleno": "BUS-1",
    })
    station = Station("N1", "정류장", city_code=22, station_no=1001)
    route = Route("R1", city_code=22, route_no="100")
    client = MagicMock()
    client._get_route_by_vehicle.return_value = route
    client._get_station_by_vehicle.return_value = station
    vehicle.bind_client(client)

    assert vehicle.route is route
    assert vehicle.station is station
    assert vehicle.gps_latitude == 35.2
    assert vehicle.gps_longitude == 128.2
