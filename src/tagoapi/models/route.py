from typing import Any, Mapping

from .base_model import BaseModel


class Route(BaseModel):
    _lazy_fields = {
        "end_vehicle_time": "_get_route",
        "start_vehicle_time": "_get_route",
        "interval_time": "_get_route",
        "interval_sat_time": "_get_route",
        "interval_sun_time": "_get_route",
        "stations": "_get_stations_by_route",
    }

    def __init__(
        self,
        route_id: str,
        city_code: int | None,
        route_no: str | None = None,
        route_type: str | None = None,
        end_node_name: str | None = None,
        start_node_name: str | None = None,
        end_vehicle_time: str | None = None,
        start_vehicle_time: str | None = None,
        interval_time: int | None = None,
        interval_sat_time: int | None = None,
        interval_sun_time: int | None = None,
    ):
        super().__init__(city_code)

        self.route_id = route_id
        self.route_no = route_no
        self.route_type = route_type
        self.end_node_name = end_node_name
        self.start_node_name = start_node_name
        self.end_vehicle_time = end_vehicle_time
        self.start_vehicle_time = start_vehicle_time
        self.interval_time = interval_time
        self.interval_sat_time = interval_sat_time
        self.interval_sun_time = interval_sun_time

    def __repr__(self) -> str:
        return f"Route({self.route_no or self.route_id})"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Route":
        return cls(
            route_id=data["routeid"],
            city_code=data.get("citycode"),
            route_no=_optional_str(data.get("routeno")),
            route_type=data.get("routetp"),
            start_node_name=data.get("startnodenm"),
            end_node_name=data.get("endnodenm"),
            end_vehicle_time=_optional_time(data.get("endvehicletime")),
            start_vehicle_time=_optional_time(data.get("startvehicletime")),
            interval_time=_optional_int(data.get("intervaltime")),
            interval_sat_time=_optional_int(data.get("intervalsattime")),
            interval_sun_time=_optional_int(data.get("intervalsuntime")),
        )


def _optional_str(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(value)


def _optional_time(value: Any) -> str | None:
    normalized = _optional_str(value)
    if normalized is None:
        return None
    return normalized.zfill(4) if normalized.isdigit() else normalized


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)
