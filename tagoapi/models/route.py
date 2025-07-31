from typing import TYPE_CHECKING
from .BaseModel import BaseModel

if TYPE_CHECKING:
    from .Station import Station


# 버스 노선 자체에 관한 정보
class Route(BaseModel):
    cache_key = "Route:<routeId>"

    def __init__(
        self,
        routeId: str,
        routeNo: str = None,
        routeTp: str = None,
        endNodeNm: str = None,
        startNodeNm: str = None,
        endvehicletime: int = None,
        startvehicletime: int = None,
        #TODO: 정류장 리스트도 넣으면 좋을 듯 합니당
    ):

        self.routeId = routeId
        self.routeNo = routeNo
        self.routeTp = routeTp
        self.endNodeNm = endNodeNm # 다른 곳에서 표시할 땐 이름으로
        self.startNodeNm = startNodeNm
        self.endvehicletime = endvehicletime
        self.startvehicletime = startvehicletime

    def __repr__(self):
        return f"Route({self.routeNo})"
    
    def to_dict(self):
        return vars(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Route":
        return cls(
            routeId=data.get("routeid"),
            routeNo=data.get("routeno"),
            routeTp=data.get("routetp"),
            startNodeNm=data.get("startnodenm"),
            endNodeNm=data.get("endnodenm"),
            endvehicletime=data.get("endvehicletime"),
            startvehicletime=data.get("startvehicletime")
        )
    
    @classmethod
    def from_list(cls, data: list[dict]) -> list["Route"]:
        return [ cls.from_dict(route) for route in data ]
