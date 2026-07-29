import csv
import gzip

import pytest

from tagoapi import StationCatalog
from tagoapi.exceptions import StationCatalogError


FIELDNAMES = [
    "정류장번호",
    "정류장명",
    "위도",
    "경도",
    "정보수집일",
    "모바일단축번호",
    "도시코드",
    "도시명",
    "관리도시명",
]


@pytest.fixture
def catalog(tmp_path):
    data_path = tmp_path / "stations.csv.gz"
    rows = [
        {
            "정류장번호": "N1",
            "정류장명": "중앙역",
            "위도": "36.1",
            "경도": "127.1",
            "정보수집일": "2024-10-28",
            "모바일단축번호": "1001",
            "도시코드": "25",
            "도시명": "도시A",
            "관리도시명": "도시A",
        },
        {
            "정류장번호": "N2",
            "정류장명": "중앙시장",
            "위도": "",
            "경도": "",
            "정보수집일": "2024-10-28",
            "모바일단축번호": "",
            "도시코드": "25",
            "도시명": "도시A",
            "관리도시명": "도시A",
        },
        {
            "정류장번호": "N3",
            "정류장명": "Central Park",
            "위도": "35.1",
            "경도": "128.1",
            "정보수집일": "2024-10-28",
            "모바일단축번호": "3001",
            "도시코드": "22",
            "도시명": "도시B",
            "관리도시명": "도시B",
        },
    ]
    _write_catalog(data_path, FIELDNAMES, rows)
    return StationCatalog._from_path(data_path)


def test_search_preserves_source_order_and_applies_limit(catalog):
    matches = catalog.search("중앙", limit=1)

    assert [station.station_id for station in matches] == ["N1"]


def test_search_filters_city_and_supports_unlimited_results(catalog):
    matches = catalog.search("central", city_code=22, limit=None)

    assert [station.station_id for station in matches] == ["N3"]


def test_get_returns_station_and_preserves_optional_empty_values(catalog):
    station = catalog.get("N2")

    assert station is not None
    assert station.station_name == "중앙시장"
    assert station.station_no is None
    assert station.gps_latitude is None
    assert station.gps_longitude is None
    assert catalog.get("missing") is None
    assert len(catalog) == 3


@pytest.mark.parametrize("keyword", ["", "   "])
def test_search_rejects_empty_keyword(catalog, keyword):
    with pytest.raises(ValueError, match="keyword"):
        catalog.search(keyword)


@pytest.mark.parametrize("limit", [0, -1, True, 1.5])
def test_search_rejects_invalid_limit(catalog, limit):
    with pytest.raises(ValueError, match="limit"):
        catalog.search("중앙", limit=limit)


def test_catalog_rejects_missing_columns(tmp_path):
    data_path = tmp_path / "invalid.csv.gz"
    _write_catalog(data_path, ["정류장번호"], [{"정류장번호": "N1"}])

    with pytest.raises(StationCatalogError, match="필수 컬럼"):
        len(StationCatalog._from_path(data_path))


def test_catalog_rejects_duplicate_station_id(tmp_path):
    data_path = tmp_path / "duplicate.csv.gz"
    duplicate = {
        "정류장번호": "N1",
        "정류장명": "중앙역",
        "위도": "36.1",
        "경도": "127.1",
        "정보수집일": "2024-10-28",
        "모바일단축번호": "",
        "도시코드": "25",
        "도시명": "도시A",
        "관리도시명": "도시A",
    }
    _write_catalog(data_path, FIELDNAMES, [duplicate, duplicate])

    with pytest.raises(StationCatalogError, match="중복"):
        len(StationCatalog._from_path(data_path))


def test_bundled_snapshot_is_available():
    catalog = StationCatalog()

    assert len(catalog) == 206_022
    station = catalog.get("ADB354000001")
    assert station is not None
    assert station.station_name == "길안정류장"
    assert station.city_code == 37040


def _write_catalog(data_path, fieldnames, rows):
    with gzip.open(data_path, mode="wt", encoding="cp949", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
