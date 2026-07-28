from typing import Any, Mapping, TYPE_CHECKING

from .base_model import BaseModel

if TYPE_CHECKING:
    from .route import Route
    from .station import Station


class Vehicle(BaseModel):
    _lazy_fields = {
        "route": "_get_route_by_vehicle",
        "station": "_get_station_by_vehicle",
    }

    def __init__(
        self,
        route_id: str,
        city_code: int | None,
        route_no: str | None = None,
        route_type: str | None = None,
        station_id: str | None = None,
        station_name: str | None = None,
        station_no: str | None = None,
        node_order: int | None = None,
        gps_latitude: float | None = None,
        gps_longitude: float | None = None,
        arrival_time: int | None = None,
        previous_station_count: int | None = None,
        vehicle_type: str | None = None,
        vehicle_no: str | None = None,
        route: "Route | None" = None,
        station: "Station | None" = None,
    ):
        super().__init__(city_code)

        self.route_id = route_id
        self.route_no = route_no
        self.route_type = route_type
        self.station_id = station_id
        self.station_name = station_name
        self.station_no = station_no
        self.node_order = node_order
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude
        self.arrival_time = arrival_time
        self.previous_station_count = previous_station_count
        self.vehicle_type = vehicle_type
        self.vehicle_no = vehicle_no
        self.route = route
        self.station = station

    def __repr__(self) -> str:
        return (
            f"Vehicle(route_id={self.route_id!r}, "
            f"vehicle_no={self.vehicle_no!r})"
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Vehicle":
        return cls(
            route_id=data["routeid"],
            city_code=data.get("citycode"),
            route_no=_optional_str(data.get("routenm", data.get("routeno"))),
            route_type=data.get("routetp"),
            station_id=data.get("nodeid"),
            station_name=data.get("nodenm"),
            station_no=_optional_str(data.get("nodeno")),
            node_order=_optional_int(data.get("nodeord")),
            gps_latitude=_optional_float(data.get("gpslati")),
            gps_longitude=_optional_float(data.get("gpslong")),
            arrival_time=_optional_int(data.get("arrtime")),
            previous_station_count=_optional_int(data.get("arrprevstationcnt")),
            vehicle_type=data.get("vehicletp"),
            vehicle_no=data.get("vehicleno"),
        )


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _optional_str(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(value)


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)
