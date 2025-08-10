from .BaseModel import BaseModel


class ArrivalInfo(BaseModel):
    def __init__(self,
        nodeId,
        nodeNm,
        routeId: str,
        routeNo: str,
        routeTp,
        arrprevstationcnt: int = None,
        vehicleTp: str = None,
        arrtime: int = None
    ):
        self.nodeId = nodeId
        self.nodeNm = nodeNm
        self.routeId = routeId
        self.routeNo = routeNo
        self.routeTp = routeTp
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
            nodeId=data.get("nodeid"),
            nodeNm=data.get("nodeid"),
            routeTp=data.get("routetp"),
            routeId = data.get("routeid"),
            routeNo = data.get("routeno"),
            arrprevstationcnt = data.get("arrprevstationcnt"),
            vehicleTp = data.get("vehicletp"),
            arrtime = data.get("arrtime")
        )
    
    @classmethod
    def from_list(cls, data: list[dict]) -> list["ArrivalInfo"]:
        return [cls.from_dict(station) for station in data]
