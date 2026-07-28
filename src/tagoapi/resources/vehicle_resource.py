from tagoapi.models import Vehicle

from .page import TagoPage
from .resource import TagoResource


class VehicleResource(TagoResource):
    middle_path = "/BusLcInfoInqireService"

    def list_by_route(
        self,
        city_code: int,
        route_id: str,
        *,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[Vehicle]:
        self._require(city_code, "city_code")
        self._require(route_id, "route_id")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            cityCode=city_code,
            routeId=route_id,
        )
        return self._request_page(
            "/getRouteAcctoBusLcList",
            params,
            model=Vehicle,
            context={"citycode": city_code, "routeid": route_id},
        )

    def list_approaching_station(
        self,
        city_code: int,
        route_id: str,
        station_id: str,
        *,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[Vehicle]:
        self._require(city_code, "city_code")
        self._require(route_id, "route_id")
        self._require(station_id, "station_id")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            cityCode=city_code,
            routeId=route_id,
            nodeId=station_id,
        )
        return self._request_page(
            "/getRouteAcctoSpcifySttnAccesBusLcInfo",
            params,
            model=Vehicle,
            context={
                "citycode": city_code,
                "routeid": route_id,
                "nodeid": station_id,
            },
        )
