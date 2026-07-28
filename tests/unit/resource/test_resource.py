from typing import Any, Mapping

import pytest

from tagoapi.exceptions import TagoResponseError, TagoServiceError
from tagoapi.models.base_model import BaseModel
from tagoapi.resources.resource import TagoResource


class ExampleModel(BaseModel):
    def __init__(self, item_id: str, city_code: int | None):
        super().__init__(city_code)
        self.item_id = item_id

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ExampleModel":
        return cls(data["id"], data.get("citycode"))


class ExampleResource(TagoResource):
    middle_path = "/ExampleService"


class FakeTransport:
    def __init__(self, response: dict):
        self.response = response
        self.calls: list[dict] = []

    def request(self, path: str, *, params: dict) -> dict:
        self.calls.append({"path": path, "params": params})
        return self.response


def _payload(item: Any, **metadata: Any) -> dict:
    return {
        "response": {
            "header": {
                "resultCode": "00",
                "resultMsg": "NORMAL SERVICE",
            },
            "body": {
                "items": {} if item is None else {"item": item},
                **metadata,
            },
        }
    }


def test_request_page_normalizes_single_item_and_preserves_metadata():
    transport = FakeTransport(
        _payload(
            {"id": "A"},
            pageNo="2",
            numOfRows="10",
            totalCount="11",
        )
    )
    resource = ExampleResource(transport)

    result = resource._request_page(
        "/list",
        {"pageNo": 2, "numOfRows": 10},
        model=ExampleModel,
        context={"citycode": 25},
    )

    assert [item.item_id for item in result.items] == ["A"]
    assert result.items[0].city_code == 25
    assert result.page_no == 2
    assert result.num_of_rows == 10
    assert result.total_count == 11
    assert transport.calls[0] == {
        "path": "/ExampleService/list",
        "params": {"pageNo": 2, "numOfRows": 10, "_type": "json"},
    }


def test_request_page_normalizes_multiple_and_empty_items():
    resource = ExampleResource(
        FakeTransport(_payload([{"id": "A"}, {"id": "B"}]))
    )
    assert len(
        resource._request_page("/list", {}, model=ExampleModel).items
    ) == 2

    empty_resource = ExampleResource(FakeTransport(_payload(None)))
    empty = empty_resource._request_page("/list", {}, model=ExampleModel)
    assert empty.items == []
    assert empty.total_count == 0


def test_request_one_rejects_multiple_items():
    resource = ExampleResource(
        FakeTransport(_payload([{"id": "A"}, {"id": "B"}]))
    )

    with pytest.raises(TagoResponseError):
        resource._request_one("/one", {}, model=ExampleModel)


def test_resource_raises_service_and_shape_errors():
    service_error = {
        "response": {
            "header": {"resultCode": "99", "resultMsg": "INVALID"},
            "body": {"items": {}},
        }
    }
    with pytest.raises(TagoServiceError) as exc_info:
        ExampleResource(FakeTransport(service_error))._request_page(
            "/list",
            {},
            model=ExampleModel,
        )
    assert exc_info.value.result_code == "99"

    malformed = _payload("not-a-mapping")
    with pytest.raises(TagoResponseError):
        ExampleResource(FakeTransport(malformed))._request_page(
            "/list",
            {},
            model=ExampleModel,
        )
