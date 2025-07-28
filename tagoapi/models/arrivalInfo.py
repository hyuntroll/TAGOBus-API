from .BaseModel import BaseModel


class ArrivalInfo(BaseModel):
    def __init__(self,
        nodeid,
        nodenm,
        routeId: str,
        routeNo: str,
        routetp,
        arrprevstationcnt: int = None,
        vehicletp: str = None,
        arrtime: int = None
    ):
        self.nodeid = nodeid
        self.nodenm = nodenm
        self.routeId = routeId
        self.routeNo = routeNo
        self.routetp = routetp
        self.arrprevstationcnt = arrprevstationcnt
        self.vehicletp = vehicletp
        self.arrtime = arrtime
    
    def __repr__(self):
        return f"ArrivalInfo({self.routeNo})"
    
    def to_dict(self):
        return vars(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "ArrivalInfo":
        return cls(
            nodeid=data.get("nodeid"),
            nodenm=data.get("nodeid"),
            routetp=data.get("routetp"),
            routeId = data.get("routeid"),
            routeNo = data.get("routeno"),
            arrprevstationcnt = data.get("arrprevstationcnt"),
            vehicletp = data.get("vehicletp"),
            arrtime = data.get("arrtime")
        )
    
    @classmethod
    def from_list(cls, data: list[dict]) -> list["ArrivalInfo"]:
        return [cls.from_dict(station) for station in data]
