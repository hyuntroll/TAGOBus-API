from typing import TYPE_CHECKING
from .BaseModel import BaseModel

class Station(BaseModel):
    # cache_key = "Station:<nodeId><nodenm>"
    cache_key = "Station:<nodeId>"
    _lazy_fields = {
        "routes": "_get_routes_by_station",
        "nodeNo": "_get_station", # csv에서 nodeId로 찾을 수 있도록 수정
    }
    
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
    ):
        super().__init__(cityCode)
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
    def from_dict(cls, data: dict) -> "Station":
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

    @property
    def node_id(self) -> str:
        return self.nodeId

    @property
    def station_id(self) -> str:
        return self.nodeId

    @property
    def node_name(self) -> str:
        return self.nodeNm

    @property
    def station_name(self) -> str:
        return self.nodeNm

    @property
    def node_no(self) -> int:
        return self.nodeNo

    @property
    def station_no(self) -> int:
        return self.nodeNo

    @property
    def gps_lati(self) -> float:
        return self.gpsLati

    @property
    def gps_long(self) -> float:
        return self.gpsLong
    
    # @classmethod
    # def from_list(cls, data: list[dict]) -> list["Station"]:
    #     return [cls.from_dict(station, client) for station in data]
    
