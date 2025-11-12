from .Route import Route
from .BaseModel import BaseModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Route import Route

class Vehicle(BaseModel):
    _lazy_fields = {
        "route": '_get_route_by_vehicle',
        "station": '_get_station_by_vehicle'
    }

    def __init__(
        self,
        cityCode: int,
        route: Route,
        gpsLati: float = None,
        gpsLong: float = None,
        arrtime: int = None,
        arrprevstationcnt: int = None,
        vehicleTp: str = None,
        vehicleNo: str = None
    ):
        super().__init__(cityCode)
        self.route = route
        self.gpsLati = gpsLati
        self.gpsLong = gpsLong
        self.arrtime = arrtime
        self.arrprevstationcnt = arrprevstationcnt
        self.vehicleTp = vehicleTp
        self.vehicleNo = vehicleNo
    
    def __repr__(self):
        return f"Vehicle({self.routeNo} - {self.vehicleNo})"
    
    def to_dict(self):
        return vars(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Vehicle":
        return cls(
            route=Route.from_dict(data),
            gpsLati=data.get("gpslati"),
            gpsLong=data.get("gpslong"),
            arrtime=data.get("arrtime"),
            arrprevstationcnt=data.get("arrprevstationcnt"),
            vehicleTp=data.get("vehicletp"),
            vehicleNo=data.get("vehicleno")
        )
    
    # @classmethod
    # def from_list(cls, data: list[dict]) -> list["Vehicle"]:
    #     return [ cls.from_dict(vehicle) for vehicle in data]