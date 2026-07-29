from unittest.mock import MagicMock

import pytest

from tagoapi import TAGOClient
from tagoapi.models import Route, Station
from tagoapi.resources import (
    ArrivalResource,
    CityResource,
    RouteResource,
    StationResource,
    TagoPage,
    VehicleResource,
)


def test_client_composes_all_resources():
    client = TAGOClient("dummy-key")
    try:
        assert isinstance(client.routes, RouteResource)
        assert isinstance(client.stations, StationResource)
        assert isinstance(client.arrivals, ArrivalResource)
        assert isinstance(client.vehicles, VehicleResource)
        assert isinstance(client.cities, CityResource)
    finally:
        client.close()


def test_legacy_route_method_delegates_without_cache():
    client = TAGOClient("dummy-key")
    route = Route("R1", city_code=25, route_no="100")
    client.routes = MagicMock()
    client.routes.list.return_value = TagoPage([route], 1, 10, 1)

    try:
        with pytest.warns(
            DeprecationWarning,
            match=r"TAGOClient\.routes\.list",
        ):
            result = client.get_route_by_no(cityCode=25, routeNo="100")
    finally:
        client.close()

    assert result == [route]
    client.routes.list.assert_called_once_with(25, "100")


def test_legacy_station_method_maps_aliases():
    client = TAGOClient("dummy-key")
    station = Station("N1", "중앙역", city_code=25, station_no="1001")
    client.stations = MagicMock()
    client.stations.list.return_value = TagoPage([station], 1, 10, 1)

    try:
        with pytest.warns(
            DeprecationWarning,
            match=r"TAGOClient\.stations\.list",
        ):
            result = client.get_station(
                cityCode=25,
                nodeNo="1001",
                nodeNm="중앙역",
            )
    finally:
        client.close()

    assert result == [station]
    client.stations.list.assert_called_once_with(
        25,
        station_no="1001",
        station_name="중앙역",
    )


def test_all_legacy_client_methods_are_marked_deprecated():
    legacy_methods = [
        "get_route_by_no",
        "get_route_by_id",
        "get_route_by_station",
        "get_station_by_route",
        "get_station",
        "get_station_by_gps",
        "get_arrival_by_station",
        "get_route_arrival_by_station",
        "get_route_pos",
        "get_route_pos_near_station",
    ]

    for method_name in legacy_methods:
        assert hasattr(getattr(TAGOClient, method_name), "__wrapped__")
