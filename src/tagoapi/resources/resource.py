from collections.abc import Mapping
from typing import Any, Protocol, TypeVar

from tagoapi.exceptions import TagoResponseError, TagoServiceError
from tagoapi.models.base_model import BaseModel

from .page import TagoPage


ModelT = TypeVar("ModelT", bound=BaseModel)


class Transport(Protocol):
    def request(self, path: str, *, params: dict[str, Any]) -> dict[str, Any]:
        ...


class TagoResource:
    middle_path: str

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def _request(
        self,
        path: str,
        params: dict[str, Any],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """하위 호환을 위한 원시 item 추출 메서드."""
        _, body = self._request_body(path, params)
        raw_items = self._extract_items(body)
        return {} if raw_items is None else raw_items

    def _request_page(
        self,
        path: str,
        params: dict[str, Any],
        *,
        model: type[ModelT],
        context: Mapping[str, Any] | None = None,
    ) -> TagoPage[ModelT]:
        request_params, body = self._request_body(path, params)
        rows = self._normalize_items(self._extract_items(body))
        models = [
            model.from_dict(self._apply_context(row, context))
            for row in rows
        ]

        return TagoPage(
            items=models,
            page_no=self._metadata_int(
                body,
                "pageNo",
                fallback=request_params.get("pageNo", 1),
            ),
            num_of_rows=self._metadata_int(
                body,
                "numOfRows",
                fallback=request_params.get("numOfRows", len(models)),
            ),
            total_count=self._metadata_int(
                body,
                "totalCount",
                fallback=len(models),
            ),
        )

    def _request_many(
        self,
        path: str,
        params: dict[str, Any],
        *,
        model: type[ModelT],
        context: Mapping[str, Any] | None = None,
    ) -> list[ModelT]:
        _, body = self._request_body(path, params)
        rows = self._normalize_items(self._extract_items(body))
        return [
            model.from_dict(self._apply_context(row, context))
            for row in rows
        ]

    def _request_one(
        self,
        path: str,
        params: dict[str, Any],
        *,
        model: type[ModelT],
        context: Mapping[str, Any] | None = None,
    ) -> ModelT | None:
        _, body = self._request_body(path, params)
        rows = self._normalize_items(self._extract_items(body))
        if not rows:
            return None
        if len(rows) != 1:
            raise TagoResponseError(
                f"단건 응답에 {len(rows)}개의 item이 포함되어 있습니다."
            )
        return model.from_dict(self._apply_context(rows[0], context))

    def _request_body(
        self,
        path: str,
        params: dict[str, Any],
    ) -> tuple[dict[str, Any], Mapping[str, Any]]:
        request_params = self._compact_params(params)
        request_params.setdefault("_type", "json")
        payload = self._transport.request(
            self.middle_path + path,
            params=request_params,
        )

        if not isinstance(payload, Mapping):
            raise TagoResponseError("TAGO 응답은 객체여야 합니다.")
        response = payload.get("response")
        if not isinstance(response, Mapping):
            raise TagoResponseError("TAGO 응답에 response 객체가 없습니다.")

        self._validate_header(response.get("header"))
        body = response.get("body")
        if not isinstance(body, Mapping):
            raise TagoResponseError("TAGO 응답에 body 객체가 없습니다.")
        return request_params, body

    @staticmethod
    def _validate_header(header: Any) -> None:
        # 과거 FakeTransport fixture에는 header가 없으므로 없을 때는 허용한다.
        if header is None:
            return
        if not isinstance(header, Mapping):
            raise TagoResponseError("TAGO response.header는 객체여야 합니다.")

        result_code = header.get("resultCode")
        if result_code is None:
            return
        normalized_code = str(result_code).zfill(2)
        if normalized_code != "00":
            result_message = header.get("resultMsg")
            raise TagoServiceError(
                normalized_code,
                None if result_message is None else str(result_message),
            )

    @staticmethod
    def _extract_items(body: Mapping[str, Any]) -> Any:
        items = body.get("items")
        if items is None or items == "":
            return None
        if not isinstance(items, Mapping):
            raise TagoResponseError("TAGO response.body.items는 객체여야 합니다.")
        return items.get("item")

    @staticmethod
    def _normalize_items(raw_items: Any) -> list[Mapping[str, Any]]:
        if raw_items is None or raw_items == "":
            return []
        if isinstance(raw_items, Mapping):
            return [raw_items]
        if isinstance(raw_items, list):
            if not all(isinstance(item, Mapping) for item in raw_items):
                raise TagoResponseError("TAGO item 목록에는 객체만 포함될 수 있습니다.")
            return raw_items
        raise TagoResponseError("TAGO item은 객체 또는 객체 목록이어야 합니다.")

    @staticmethod
    def _apply_context(
        row: Mapping[str, Any],
        context: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        normalized = dict(row)
        for key, value in (context or {}).items():
            if value is not None:
                normalized.setdefault(key, value)
        return normalized

    @staticmethod
    def _compact_params(params: Mapping[str, Any]) -> dict[str, Any]:
        return {
            key: value
            for key, value in params.items()
            if value is not None
        }

    @staticmethod
    def _metadata_int(
        body: Mapping[str, Any],
        key: str,
        *,
        fallback: Any,
    ) -> int:
        value = body.get(key, fallback)
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise TagoResponseError(
                f"TAGO response.body.{key}는 정수여야 합니다."
            ) from exc

    @staticmethod
    def _page_params(
        *,
        page_no: int,
        num_of_rows: int,
        **params: Any,
    ) -> dict[str, Any]:
        if page_no < 1:
            raise ValueError("page_no는 1 이상이어야 합니다.")
        if num_of_rows < 1:
            raise ValueError("num_of_rows는 1 이상이어야 합니다.")
        return {
            "pageNo": page_no,
            "numOfRows": num_of_rows,
            **params,
        }

    @staticmethod
    def _require(value: Any, parameter_name: str) -> None:
        if value is None or value == "":
            raise ValueError(f"{parameter_name}은(는) 필수입니다.")
