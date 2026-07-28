from typing import Any, Mapping

from .base_model import BaseModel


class Station(BaseModel):
    _lazy_fields = {
        "station_no": "_get_station",
        "gps_latitude": "_get_station",
        "gps_longitude": "_get_station",
        "routes": "_get_routes_by_station",
    }

    def __init__(
        self,
        station_id: str,
        station_name: str,
        city_code: int | None = None,
        station_no: str | None = None,
        gps_latitude: float | None = None,
        gps_longitude: float | None = None,
        up_down_code: int | None = None,
        node_order: int | None = None,
    ):
        super().__init__(city_code)

        self.station_id = station_id
        self.station_name = station_name
        self.station_no = station_no
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude
        self.up_down_code = up_down_code
        self.node_order = node_order

    def __repr__(self) -> str:
        return f"Station({self.station_name})"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Station":
        return cls(
            station_id=data["nodeid"],
            station_name=data["nodenm"],
            city_code=_optional_int(data.get("citycode")),
            station_no=_optional_str(data.get("nodeno")),
            gps_latitude=_optional_float(data.get("gpslati")),
            gps_longitude=_optional_float(data.get("gpslong")),
            up_down_code=_optional_int(data.get("updowncd")),
            node_order=_optional_int(data.get("nodeord")),
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
