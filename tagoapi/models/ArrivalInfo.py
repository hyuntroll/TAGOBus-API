from .BaseModel import BaseModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Station import Station
    from .Route import Route


class ArrivalInfo(BaseModel):
    _lazy_fields = {
        "station": "_get_station_by_arrival_info",
        "routes": "_get_route_by_arrival_info"
    }

    def __init__(self,
        node: "Station",
        route: "Route",
        cityCode,
        arrprevstationcnt: int = None,
        vehicleTp: str = None,
        arrtime: int = None
    ):
        super().__init__(cityCode)
        self.node = node
        self.route = route
        self.arrprevstationcnt = arrprevstationcnt
        self.vehicleTp = vehicleTp
        self.arrtime = arrtime
    
    def __repr__(self):
        return f"ArrivalInfo({self.routeNo})"
    
    def to_dict(self):
        return vars(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "ArrivalInfo":
        return cls(
            node=Station.from_dict(data),
            route=Route.from_dict(data["route"]),
            arrprevstationcnt = data.get("arrprevstationcnt"),
            vehicleTp = data.get("vehicletp"),
            arrtime = data.get("arrtime")
        )
    
    # @classmethod
    # def from_list(cls, data: list[dict]) -> list["ArrivalInfo"]:
    #     return [cls.from_dict(station) for station in data]
