from tagoapi.models import ArrivalInfo, CityCode, Route, Station, Vehicle


def test_route_maps_flat_payload():
    route = Route.from_dict({
        "routeid": "R1",
        "citycode": 22,
        "routeno": "100",
        "endvehicletime": 2330,
        "startvehicletime": 530,
    })

    assert route.end_vehicle_time == "2330"
    assert route.start_vehicle_time == "0530"


def test_station_allows_missing_coordinates():
    station = Station.from_dict({
        "nodeid": "N1",
        "nodenm": "정류장",
        "citycode": 22,
    })

    assert station.station_no is None
    assert station.gps_latitude is None
    assert station.gps_longitude is None


def test_arrival_maps_flat_payload():
    arrival = ArrivalInfo.from_dict({
        "nodeid": "N1",
        "routeid": "R1",
        "citycode": 22,
        "nodeno": 1001,
        "arrprevstationcnt": 2,
        "vehicletp": "일반",
        "arrtime": 180,
    })

    assert arrival.station is None
    assert arrival.route is None
    assert arrival.previous_station_count == 2


def test_vehicle_maps_flat_payload():
    vehicle = Vehicle.from_dict({
        "routeid": "R1",
        "citycode": 22,
        "nodeno": 1001,
        "gpslati": "35.2",
        "gpslong": "128.2",
        "vehicleno": "BUS-1",
    })

    assert vehicle.route is None
    assert vehicle.station is None
    assert vehicle.gps_latitude == 35.2
    assert vehicle.gps_longitude == 128.2


def test_city_code_maps_documented_payload():
    city = CityCode.from_dict({
        "citycode": "22",
        "cityname": "대구광역시",
    })

    assert city.city_code == 22
    assert city.city_name == "대구광역시"
    assert city.to_dict() == {
        "city_code": 22,
        "city_name": "대구광역시",
    }
