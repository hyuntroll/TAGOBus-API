from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .route import Route

class Station:
    def __init__(
        self,
        nodeId: str,
        nodeNm: str,
        nodeNo: int = None,
        gpsLati: float = None,
        gpsLong: float = None,
        # *routeList: list['Route']
    ):
        self.nodeId = nodeId
        self.nodeNm = nodeNm
        self.nodeNo = nodeNo
        self.gpsLati = gpsLati
        self.gpsLong = gpsLong
        # self.routeList = routeList

    def __repr__(self):
        return f"<Station {self.nodeNm}>"
    
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

        )
    