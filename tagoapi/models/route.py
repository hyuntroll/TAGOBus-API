# 버스 노선 자체에 관한 정보
class Route:
    def __init__(self, data: dict):
        self.routeId = data.get("routeid")
        self.routeNo = data.get("routeno")
        self.routeTp = data.get("routetp")
        self.endnode = data.get("endnode") # 다른 곳에서 표시할 땐 이름으로
        self.startnode = data.get("startnode")
        self.endvhicletime = data.get("endvhicletime")
        self.startvehicletime = data.get("startvehicletime")

    def __repr__(self):
        return f"<Route {self.routeNo}>"