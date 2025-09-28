from typing import TYPE_CHECKING
from .BaseModel import BaseModel
if TYPE_CHECKING:
    from .Route import Route
    from tagoapi import TAGOClient

class Station(BaseModel):
    # cache_key = "Station:<nodeId><nodenm>"
    cache_key = "Station:<nodeId>"
    
    def __init__(
        self,
        nodeId: str,
        nodeNm: str,
        nodeNo: int = None,
        gpsLati: float = None,
        gpsLong: float = None,
        cityCode: int = None,
        updowncd: int = None,
        nodeord: int = None,
        # *routeList: list['Route']
    ):
        super().__init__()
        self.nodeId = nodeId
        self.nodeNm = nodeNm
        self.nodeNo = nodeNo
        self.gpsLati = gpsLati
        self.gpsLong = gpsLong
        self.cityCode = cityCode
        self.updowncd = updowncd
        self.nodeord = nodeord
        # self.routeList = routeList

    def __repr__(self):
        return f"Station({self.nodeNm})"
    
    def to_dict(self):
        return vars(self)
    
    @classmethod
    def from_dict(cls, data: dict, client: "TAGOClient") -> "Station":
        return cls(
            nodeId = data.get("nodeid"),
            nodeNm = data.get("nodenm"),
            nodeNo = data.get("nodeno"),
            gpsLati = float(data.get("gpslati")),
            gpsLong = float(data.get("gpslong")),
            cityCode = data.get("citycode"),
            updowncd = data.get("updowncd"),
            nodeord = data.get("nodeord"),
        )
    
    @classmethod
    def from_list(cls, data: list[dict], client: "TAGOClient") -> list["Station"]:
        return [cls.from_dict(station, client) for station in data]
    