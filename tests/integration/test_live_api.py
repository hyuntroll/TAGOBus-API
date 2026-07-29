import os

import pytest

from tagoapi import TAGOClient


pytestmark = pytest.mark.integration


def test_live_resource_flow():
    if os.getenv("TAGO_RUN_INTEGRATION") != "1":
        pytest.skip("TAGO_RUN_INTEGRATION=1일 때만 실 API 테스트를 실행합니다.")

    service_key = os.getenv("TAGO_API_KEY")
    if not service_key:
        pytest.fail("실 API 테스트에는 TAGO_API_KEY가 필요합니다.")

    city_code = int(os.getenv("TAGO_TEST_CITY_CODE", "25"))
    route_no = os.getenv("TAGO_TEST_ROUTE_NO", "100")

    with TAGOClient(service_key=service_key) as client:
        cities = client.cities.list()
        assert any(city.city_code == city_code for city in cities)

        routes = client.routes.list(
            city_code=city_code,
            route_no=route_no,
            num_of_rows=10,
        )
        assert routes.items

        route = routes.items[0]
        route_detail = client.routes.get(city_code, route.route_id)
        assert route_detail is not None
        assert route_detail.route_id == route.route_id

        stations = client.routes.list_stations(
            city_code=city_code,
            route_id=route.route_id,
            num_of_rows=100,
        )
        assert stations.items

        station = stations.items[0]
        arrivals = client.arrivals.list_by_station(
            city_code=city_code,
            station_id=station.station_id,
        )
        assert arrivals.total_count >= len(arrivals.items)

        vehicles = client.vehicles.list_by_route(
            city_code=city_code,
            route_id=route.route_id,
        )
        assert vehicles.total_count >= len(vehicles.items)
