from tagoapi.models import ArrivalInfo

from .page import TagoPage
from .resource import TagoResource


class ArrivalResource(TagoResource):
    middle_path = "/ArvlInfoInqireService"

    def list_by_station(
        self,
        city_code: int,
        station_id: str,
        *,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[ArrivalInfo]:
        self._require(city_code, "city_code")
        self._require(station_id, "station_id")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            cityCode=city_code,
            nodeId=station_id,
        )
        return self._request_page(
            "/getSttnAcctoArvlPrearngeInfoList",
            params,
            model=ArrivalInfo,
            context={"citycode": city_code, "nodeid": station_id},
        )

    def list_by_station_and_route(
        self,
        city_code: int,
        station_id: str,
        route_id: str,
        *,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[ArrivalInfo]:
        self._require(city_code, "city_code")
        self._require(station_id, "station_id")
        self._require(route_id, "route_id")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            cityCode=city_code,
            nodeId=station_id,
            routeId=route_id,
        )
        return self._request_page(
            "/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList",
            params,
            model=ArrivalInfo,
            context={
                "citycode": city_code,
                "nodeid": station_id,
                "routeid": route_id,
            },
        )
