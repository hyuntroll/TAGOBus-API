from tagoapi.models import CityCode

from .resource import TagoResource


class CityResource(TagoResource):
    """TAGO 서비스 가능 도시코드 조회."""

    middle_path = "/BusRouteInfoInqireService"

    def list(self) -> list[CityCode]:
        return self._request_many(
            "/getCtyCodeList",
            {},
            model=CityCode,
        )
