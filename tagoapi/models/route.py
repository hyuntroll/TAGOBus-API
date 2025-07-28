from typing import TYPE_CHECKING
from .BaseModel import BaseModel

if TYPE_CHECKING:
    from tagoapi import TAGOClient
    from .Station import Station


# 버스 노선 자체에 관한 정보
class Route(BaseModel):
    cache_key = "Route:<routeId>"

    def __init__(
        self,
        routeId: str,
        client: "TAGOClient",
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
        self._client = client


    def __repr__(self):
        return f"Route({self.routeNo})"
    
    @property
    def endStation(self) -> "Station":
        return self._client.get_station(cityCode=22, nodeNm=self.endNodeNm)

    @classmethod
    def from_dict(cls, data: dict, client) -> "Route":
        return cls(
            routeId=data["routeid"],
            routeNo=data["routeno"],
            routeTp=data["routetp"],
            startNodeNm=data.get("startnodenm"),
            endNodeNm=data.get("endnodenm"),
            endvehicletime=data.get("endvehicletime"),
            startvehicletime=data.get("startvehicletime"),
            client=client
        )
    
    @classmethod
    def from_list(cls, data: list[dict], client) -> list["Route"]:
        return [ cls.from_dict(route, client) for route in data ]
