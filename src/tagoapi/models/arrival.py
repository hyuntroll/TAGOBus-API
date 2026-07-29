from typing import Any, Mapping, TYPE_CHECKING

from .base_model import BaseModel

if TYPE_CHECKING:
    from .route import Route
    from .station import Station


class ArrivalInfo(BaseModel):
    def __init__(
        self,
        station_id: str,
        route_id: str,
        city_code: int | None,
        station_no: str | None = None,
        station_name: str | None = None,
        route_no: str | None = None,
        route_type: str | None = None,
        previous_station_count: int | None = None,
        vehicle_type: str | None = None,
        arrival_time: int | None = None,
        station: "Station | None" = None,
        route: "Route | None" = None,
    ):
        super().__init__(city_code)

        self.station_id = station_id
        self.route_id = route_id
        self.station_no = station_no
        self.station_name = station_name
        self.route_no = route_no
        self.route_type = route_type
        self.previous_station_count = previous_station_count
        self.vehicle_type = vehicle_type
        self.arrival_time = arrival_time
        self.station = station
        self.route = route

    def __repr__(self) -> str:
        return (
            f"ArrivalInfo(route_id={self.route_id!r}, "
            f"station_id={self.station_id!r})"
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ArrivalInfo":
        return cls(
            station_id=data["nodeid"],
            route_id=data["routeid"],
            city_code=data.get("citycode"),
            station_no=_optional_str(data.get("nodeno")),
            station_name=data.get("nodenm"),
            route_no=_optional_str(data.get("routeno")),
            route_type=data.get("routetp"),
            previous_station_count=_optional_int(data.get("arrprevstationcnt")),
            vehicle_type=data.get("vehicletp"),
            arrival_time=_optional_int(data.get("arrtime")),
        )


def _optional_str(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(value)


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)
