from typing import Any

from ._internal import HttpTransport
from .models import ArrivalInfo, Route, Station, Vehicle
from .resources import (
    ArrivalResource,
    CityResource,
    RouteResource,
    StationResource,
    VehicleResource,
)


class TAGOClient:
    """TAGO 전송 계층과 서비스별 Resource를 조립하는 진입점."""

    BASE_URL = "http://apis.data.go.kr/1613000"

    def __init__(self, service_key: str) -> None:
        if not service_key:
            raise ValueError("service_key는 필수입니다.")

        self._transport = HttpTransport(
            base_url=self.BASE_URL,
            service_key=service_key,
        )
        self.routes = RouteResource(self._transport)
        self.stations = StationResource(self._transport)
        self.arrivals = ArrivalResource(self._transport)
        self.vehicles = VehicleResource(self._transport)
        self.cities = CityResource(self._transport)

    def __enter__(self) -> "TAGOClient":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def close(self) -> None:
        self._transport.close()

    # 기존 공개 메서드는 cache 없이 새 Resource로 위임한다.
    def get_route_by_no(
        self,
        city_code: int | None = None,
        route_no: str | None = None,
        *,
        cityCode: int | None = None,
        routeNo: str | None = None,
    ) -> list[Route]:
        normalized_city_code = self._coalesce(city_code, cityCode)
        normalized_route_no = self._coalesce(route_no, routeNo)
        return self.routes.list(
            normalized_city_code,
            normalized_route_no,
        ).items

    def get_route_by_id(
        self,
        city_code: int | None = None,
        route_id: str | None = None,
        *,
        cityCode: int | None = None,
        routeId: str | None = None,
    ) -> Route | None:
        return self.routes.get(
            self._coalesce(city_code, cityCode),
            self._coalesce(route_id, routeId),
        )

    def get_route_by_station(
        self,
        city_code: int | None = None,
        station_id: str | None = None,
        *,
        cityCode: int | None = None,
        nodeId: str | None = None,
    ) -> list[Route]:
        return self.stations.list_routes(
            self._coalesce(city_code, cityCode),
            self._coalesce(station_id, nodeId),
        ).items

    def get_station_by_route(
        self,
        city_code: int | None = None,
        route_id: str | None = None,
        *,
        cityCode: int | None = None,
        routeId: str | None = None,
    ) -> list[Station]:
        return self.routes.list_stations(
            self._coalesce(city_code, cityCode),
            self._coalesce(route_id, routeId),
        ).items

    def get_station(
        self,
        city_code: int | None = None,
        station_no: str | int | None = None,
        station_name: str | None = None,
        *,
        cityCode: int | None = None,
        nodeNo: str | int | None = None,
        nodeNm: str | None = None,
    ) -> list[Station]:
        return self.stations.list(
            self._coalesce(city_code, cityCode),
            station_no=self._coalesce(station_no, nodeNo),
            station_name=self._coalesce(station_name, nodeNm),
        ).items

    def get_station_by_gps(
        self,
        gps_lati: float | None = None,
        gps_long: float | None = None,
        *,
        gpsLati: float | None = None,
        gpsLong: float | None = None,
    ) -> list[Station]:
        return self.stations.list_nearby(
            self._coalesce(gps_lati, gpsLati),
            self._coalesce(gps_long, gpsLong),
        ).items

    def get_arrival_by_station(
        self,
        city_code: int | None = None,
        station_id: str | None = None,
        node_id: str | None = None,
        *,
        cityCode: int | None = None,
        nodeId: str | None = None,
    ) -> list[ArrivalInfo]:
        return self.arrivals.list_by_station(
            self._coalesce(city_code, cityCode),
            self._coalesce(station_id, node_id, nodeId),
        ).items

    def get_route_arrival_by_station(
        self,
        city_code: int | None = None,
        station_id: str | None = None,
        node_id: str | None = None,
        route_id: str | None = None,
        *,
        cityCode: int | None = None,
        nodeId: str | None = None,
        routeId: str | None = None,
    ) -> list[ArrivalInfo]:
        return self.arrivals.list_by_station_and_route(
            self._coalesce(city_code, cityCode),
            self._coalesce(station_id, node_id, nodeId),
            self._coalesce(route_id, routeId),
        ).items

    def get_route_pos(
        self,
        city_code: int | None = None,
        route_id: str | None = None,
        *,
        cityCode: int | None = None,
        routeId: str | None = None,
    ) -> list[Vehicle]:
        return self.vehicles.list_by_route(
            self._coalesce(city_code, cityCode),
            self._coalesce(route_id, routeId),
        ).items

    def get_route_pos_near_station(
        self,
        city_code: int | None = None,
        route_id: str | None = None,
        station_id: str | None = None,
        node_id: str | None = None,
        *,
        cityCode: int | None = None,
        routeId: str | None = None,
        nodeId: str | None = None,
    ) -> list[Vehicle]:
        return self.vehicles.list_approaching_station(
            self._coalesce(city_code, cityCode),
            self._coalesce(route_id, routeId),
            self._coalesce(station_id, node_id, nodeId),
        ).items

    # BaseModel lazy loading을 다시 연결할 때 사용할 기존 loader 계약.
    def _get_route(self, route: Route) -> Route | None:
        return self.routes.get(route.city_code, route.route_id)

    def _get_stations_by_route(self, route: Route) -> list[Station]:
        return self.routes.list_stations(
            route.city_code,
            route.route_id,
        ).items

    def _get_station(self, station: Station) -> Station | None:
        stations = self.stations.list(
            station.city_code,
            station_no=station.station_no,
            station_name=station.station_name,
        ).items
        return stations[0] if stations else None

    def _get_routes_by_station(self, station: Station) -> list[Route]:
        return self.stations.list_routes(
            station.city_code,
            station.station_id,
        ).items

    def _get_station_by_arrival_info(
        self,
        arrival_info: ArrivalInfo,
    ) -> Station | None:
        stations = self.stations.list(
            arrival_info.city_code,
            station_no=arrival_info.station_no,
            station_name=arrival_info.station_name,
        ).items
        return stations[0] if stations else None

    def _get_route_by_arrival_info(
        self,
        arrival_info: ArrivalInfo,
    ) -> Route | None:
        return self.routes.get(
            arrival_info.city_code,
            arrival_info.route_id,
        )

    def _get_route_by_vehicle(self, vehicle: Vehicle) -> Route | None:
        return self.routes.get(vehicle.city_code, vehicle.route_id)

    def _get_station_by_vehicle(self, vehicle: Vehicle) -> Station | None:
        if vehicle.station_id:
            stations = self.stations.list(
                vehicle.city_code,
                station_name=vehicle.station_name,
            ).items
        else:
            stations = self.stations.list(
                vehicle.city_code,
                station_no=vehicle.station_no,
                station_name=vehicle.station_name,
            ).items
        return stations[0] if stations else None

    def _get(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        """이전 테스트 및 확장 코드를 위한 Transport 위임 메서드."""
        path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        return self._transport.request(path, params=params)

    @staticmethod
    def _coalesce(*values: Any) -> Any:
        for value in values:
            if value is not None:
                return value
        return None
