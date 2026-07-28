from tagoapi.models import Route, Station

from .page import TagoPage
from .resource import TagoResource


class RouteResource(TagoResource):
    middle_path = "/BusRouteInfoInqireService"

    def list(
        self,
        city_code: int,
        route_no: str | None = None,
        *,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[Route]:
        self._require(city_code, "city_code")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            cityCode=city_code,
            routeNo=route_no,
        )
        return self._request_page(
            "/getRouteNoList",
            params,
            model=Route,
            context={"citycode": city_code},
        )

    def get(self, city_code: int, route_id: str) -> Route | None:
        self._require(city_code, "city_code")
        self._require(route_id, "route_id")
        return self._request_one(
            "/getRouteInfoIem",
            {"cityCode": city_code, "routeId": route_id},
            model=Route,
            context={"citycode": city_code, "routeid": route_id},
        )

    def list_stations(
        self,
        city_code: int,
        route_id: str,
        *,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[Station]:
        self._require(city_code, "city_code")
        self._require(route_id, "route_id")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            cityCode=city_code,
            routeId=route_id,
        )
        return self._request_page(
            "/getRouteAcctoThrghSttnList",
            params,
            model=Station,
            context={"citycode": city_code},
        )
