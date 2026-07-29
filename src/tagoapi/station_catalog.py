from collections import defaultdict
import csv
from dataclasses import dataclass, field
import gzip
from importlib import resources

from .exceptions import StationCatalogError
from .models import Station


_DATA_FILE = "stations_2025_06_15.csv.gz"


@dataclass(slots=True)
class _StationRecord:
    station_id: str
    station_name: str
    station_no: str | None
    gps_latitude: float | None
    gps_longitude: float | None
    city_code: int
    normalized_name: str = field(init=False)

    def __post_init__(self) -> None:
        self.normalized_name = self.station_name.casefold()

    def to_station(self) -> Station:
        return Station(
            station_id=self.station_id,
            station_name=self.station_name,
            city_code=self.city_code,
            station_no=self.station_no,
            gps_latitude=self.gps_latitude,
            gps_longitude=self.gps_longitude,
        )


class StationCatalog:
    """Bundled official station snapshot for fast, offline lookup."""

    snapshot_date = "2025-06-15"
    information_date = "2024-10-28"

    def __init__(self) -> None:
        self._records: tuple[_StationRecord, ...] | None = None
        self._station_id_index: dict[str, int] = {}
        self._city_index: dict[int, tuple[int, ...]] = {}

    def search(
        self,
        keyword: str,
        *,
        city_code: int | None = None,
        limit: int | None = 100,
    ) -> list[Station]:
        normalized_keyword = keyword.strip().casefold()
        if not normalized_keyword:
            raise ValueError("keyword는 비어 있을 수 없습니다.")
        if limit is not None and (
            isinstance(limit, bool)
            or not isinstance(limit, int)
            or limit < 1
        ):
            raise ValueError("limit은 1 이상의 정수 또는 None이어야 합니다.")

        self._ensure_loaded()
        records = self._loaded_records()
        candidate_indices: range | tuple[int, ...]
        if city_code is None:
            candidate_indices = range(len(records))
        else:
            candidate_indices = self._city_index.get(city_code, ())

        matches: list[Station] = []
        for index in candidate_indices:
            record = records[index]
            if normalized_keyword not in record.normalized_name:
                continue
            matches.append(record.to_station())
            if limit is not None and len(matches) >= limit:
                break
        return matches

    def get(self, station_id: str) -> Station | None:
        normalized_station_id = station_id.strip()
        if not normalized_station_id:
            raise ValueError("station_id는 비어 있을 수 없습니다.")

        self._ensure_loaded()
        index = self._station_id_index.get(normalized_station_id)
        if index is None:
            return None
        return self._loaded_records()[index].to_station()

    def __len__(self) -> int:
        self._ensure_loaded()
        return len(self._loaded_records())

    def _ensure_loaded(self) -> None:
        if self._records is not None:
            return

        records: list[_StationRecord] = []
        station_id_index: dict[str, int] = {}
        city_index: defaultdict[int, list[int]] = defaultdict(list)

        try:
            data_file = resources.files("tagoapi.data").joinpath(_DATA_FILE)
            with (
                data_file.open("rb") as compressed_stream,
                gzip.open(
                    compressed_stream,
                    mode="rt",
                    encoding="cp949",
                    newline="",
                ) as stream,
            ):
                reader = csv.DictReader(stream)
                for row in reader:
                    record = self._parse_record(row)
                    index = len(records)
                    records.append(record)
                    station_id_index[record.station_id] = index
                    city_index[record.city_code].append(index)
        except (OSError, UnicodeError, csv.Error, KeyError, ValueError) as exc:
            raise StationCatalogError(
                "정류소 데이터를 읽을 수 없습니다."
            ) from exc

        self._records = tuple(records)
        self._station_id_index = station_id_index
        self._city_index = {
            city_code: tuple(indices)
            for city_code, indices in city_index.items()
        }

    @staticmethod
    def _parse_record(row: dict[str, str | None]) -> _StationRecord:
        station_id = (row.get("정류장번호") or "").strip()
        station_name = (row.get("정류장명") or "").strip()
        station_no = (row.get("모바일단축번호") or "").strip() or None
        return _StationRecord(
            station_id=station_id,
            station_name=station_name,
            station_no=station_no,
            gps_latitude=_optional_float(row.get("위도")),
            gps_longitude=_optional_float(row.get("경도")),
            city_code=int((row.get("도시코드") or "").strip()),
        )

    def _loaded_records(self) -> tuple[_StationRecord, ...]:
        records = self._records
        if records is None:
            raise RuntimeError("StationCatalog 데이터가 초기화되지 않았습니다.")
        return records


def _optional_float(value: str | None) -> float | None:
    normalized = (value or "").strip()
    if not normalized:
        return None
    return float(normalized)
