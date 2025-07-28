from .Route import Route
from .BaseModel import BaseModel

class Vehicle(BaseModel):
    def __init__(
        self,
        route: Route = None, 
        routeId: str = None,
        routeNo: str = None,
        gpsLati: float = None,
        gpsLong: float = None,
        arrtime: int = None,
        arrprevstationcnt: int = None,
        vehicleTp: str = None,
        vehicleNo: str = None
    ):
        self.route = route
        self.routeId = routeId
        self.routeNo = routeNo
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
            route=data.get("route"),
            routeId=data.get("routeid"),
            routeNo=data.get("routeno", data.get("routenm")),
            gpsLati=data.get("gpslati"),
            gpsLong=data.get("gpslong"),
            arrtime=data.get("arrtime"),
            arrprevstationcnt=data.get("arrprevstationcnt"),
            vehicleTp=data.get("vehicletp"),
            vehicleNo=data.get("vehicleno")
        )
    
    @classmethod
    def from_list(cls, data:list[dict]) -> list["Vehicle"]:
        return [ cls.from_dict(vehicle) for vehicle in data]