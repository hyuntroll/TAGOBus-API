import pytest

from tagoapi import StationCatalog


@pytest.fixture(scope="module")
def catalog():
    return StationCatalog()


def test_search_preserves_source_order_and_applies_limit(catalog):
    matches = catalog.search("종합버스터미널", city_code=12, limit=1)

    assert [station.station_id for station in matches] == ["SJB286066009"]


def test_search_filters_city_and_supports_unlimited_results(catalog):
    matches = catalog.search("길안", city_code=37040, limit=None)

    assert any(station.station_id == "ADB354000001" for station in matches)
    assert catalog.search("길안", city_code=-1) == []


def test_get_returns_station_and_preserves_optional_empty_values(catalog):
    station = catalog.get("SJB270054818")

    assert station is not None
    assert station.station_name == "부모산,연화사입구"
    assert station.gps_latitude is None
    assert station.gps_longitude is None
    assert catalog.get("missing") is None


@pytest.mark.parametrize("keyword", ["", "   "])
def test_search_rejects_empty_keyword(catalog, keyword):
    with pytest.raises(ValueError, match="keyword"):
        catalog.search(keyword)


@pytest.mark.parametrize("limit", [0, -1, True, 1.5])
def test_search_rejects_invalid_limit(catalog, limit):
    with pytest.raises(ValueError, match="limit"):
        catalog.search("중앙", limit=limit)


def test_bundled_snapshot_is_available(catalog):
    assert len(catalog) == 206_022
    station = catalog.get("ADB354000001")
    assert station is not None
    assert station.station_name == "길안정류장"
    assert station.city_code == 37040
