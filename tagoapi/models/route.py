from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .station import Station

# 버스 노선 자체에 관한 정보
class Route:
    def __init__(
        self,
        routeId: str,
        routeNo: str = None,
        routeTp: str = None,
        endNode: "Station" = None,
        startNode: "Station" = None,
        endvehicletime: int = None,
        startvehicletime: int = None,
        #TODO: 정류장 리스트도 넣으면 좋을 듯 합니당
    ):

        self.routeId = routeId
        self.routeNo = routeNo
        self.routeTp = routeTp # 버스 종류는 저장 안해도 될듯;
        self.endnode = endNode # 다른 곳에서 표시할 땐 이름으로
        self.startnode = startNode
        self.endvehicletime = endvehicletime
        self.startvehicletime = startvehicletime

    def __repr__(self):
        return f"<Route: {self.routeNo}>"
    
    def to_dict(self):
        return vars(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Route":
        return cls(
            routeId=data["routeid"],
            routeNo=data["routeno"],
            routeTp=data["routetp"],
            endvehicletime=data.get("endvehicletime"),
            startvehicletime=data.get("startvehicletime")
        )
    
    @classmethod
    def from_list(cls, data: list[dict]) -> list["Route"]:
        return [ cls.from_dict(route) for route in data ]