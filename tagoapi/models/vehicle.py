from .route import Route


class Vehicle:
    def __init__(self, route: Route, data: dict):
        self.route = route 
        self.gpsLati = data.get("gpslati")
        self.gpsLong = data.get("gpslong")
        self.nodeOrd = data.get("nodeord")
        self.vehicleNo = data.get("vehicleno") # 다른 곳에서 표시할 때 이 이름도 함께
    
    def __repr__(self):
        return f"<Route {self.route.routeNo} - {self.vehicleNo}>"