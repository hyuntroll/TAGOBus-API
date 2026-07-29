from tagoapi.models import Route, Station

from .page import TagoPage
from .resource import TagoResource


class StationResource(TagoResource):
    middle_path = "/BusSttnInfoInqireService"

    def list(
        self,
        city_code: int,
        *,
        station_name: str | None = None,
        station_no: str | int | None = None,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[Station]:
        self._require(city_code, "city_code")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            cityCode=city_code,
            nodeNm=station_name,
            nodeNo=station_no,
        )
        return self._request_page(
            "/getSttnNoList",
            params,
            model=Station,
            context={"citycode": city_code},
        )

    def list_nearby(
        self,
        gps_latitude: float,
        gps_longitude: float,
        *,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[Station]:
        self._require(gps_latitude, "gps_latitude")
        self._require(gps_longitude, "gps_longitude")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            gpsLati=gps_latitude,
            gpsLong=gps_longitude,
        )
        return self._request_page(
            "/getCrdntPrxmtSttnList",
            params,
            model=Station,
        )

    def list_routes(
        self,
        city_code: int,
        station_id: str,
        *,
        page_no: int = 1,
        num_of_rows: int = 10,
    ) -> TagoPage[Route]:
        self._require(city_code, "city_code")
        self._require(station_id, "station_id")
        params = self._page_params(
            page_no=page_no,
            num_of_rows=num_of_rows,
            cityCode=city_code,
            nodeid=station_id,
        )
        return self._request_page(
            "/getSttnThrghRouteList",
            params,
            model=Route,
            context={"citycode": city_code},
        )
