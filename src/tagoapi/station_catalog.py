from collections import defaultdict
from contextlib import contextmanager
import csv
import gzip
from importlib import resources
from pathlib import Path
from typing import Iterator, Mapping, TextIO

from .exceptions import StationCatalogError
from .models import Station


_DATA_FILE = "stations_2025_06_15.csv.gz"
_REQUIRED_COLUMNS = frozenset(
    {
        "정류장번호",
        "정류장명",
        "위도",
        "경도",
        "모바일단축번호",
        "도시코드",
    }
)


class _StationRecord:
    __slots__ = (
        "station_id",
        "station_name",
        "normalized_name",
        "station_no",
        "gps_latitude",
        "gps_longitude",
        "city_code",
    )

    def __init__(
        self,
        *,
        station_id: str,
        station_name: str,
        station_no: str | None,
        gps_latitude: float | None,
        gps_longitude: float | None,
        city_code: int,
    ) -> None:
        self.station_id = station_id
        self.station_name = station_name
        self.normalized_name = station_name.casefold()
        self.station_no = station_no
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude
        self.city_code = city_code

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
        self._data_path: Path | None = None
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

    @classmethod
    def _from_path(cls, data_path: Path) -> "StationCatalog":
        catalog = cls()
        catalog._data_path = data_path
        return catalog

    def _ensure_loaded(self) -> None:
        if self._records is not None:
            return

        records: list[_StationRecord] = []
        station_id_index: dict[str, int] = {}
        city_index: defaultdict[int, list[int]] = defaultdict(list)

        try:
            with self._open_data() as stream:
                reader = csv.DictReader(stream)
                columns = frozenset(reader.fieldnames or ())
                missing_columns = _REQUIRED_COLUMNS - columns
                if missing_columns:
                    names = ", ".join(sorted(missing_columns))
                    raise StationCatalogError(
                        f"정류소 데이터에 필수 컬럼이 없습니다: {names}"
                    )

                for row_number, row in enumerate(reader, start=2):
                    record = self._parse_record(row, row_number)
                    if record.station_id in station_id_index:
                        raise StationCatalogError(
                            f"{row_number}행의 정류장번호가 중복되었습니다: "
                            f"{record.station_id}"
                        )
                    index = len(records)
                    records.append(record)
                    station_id_index[record.station_id] = index
                    city_index[record.city_code].append(index)
        except StationCatalogError:
            raise
        except (OSError, UnicodeError, csv.Error) as exc:
            raise StationCatalogError(
                "정류소 데이터를 읽을 수 없습니다."
            ) from exc

        self._records = tuple(records)
        self._station_id_index = station_id_index
        self._city_index = {
            city_code: tuple(indices)
            for city_code, indices in city_index.items()
        }

    @contextmanager
    def _open_data(self) -> Iterator[TextIO]:
        if self._data_path is not None:
            with gzip.open(
                self._data_path,
                mode="rt",
                encoding="cp949",
                newline="",
            ) as stream:
                yield stream
            return

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
            yield stream

    @staticmethod
    def _parse_record(
        row: Mapping[str, str | None],
        row_number: int,
    ) -> _StationRecord:
        station_id = (row.get("정류장번호") or "").strip()
        station_name = (row.get("정류장명") or "").strip()
        if not station_id:
            raise StationCatalogError(
                f"{row_number}행의 정류장번호가 비어 있습니다."
            )
        if not station_name:
            raise StationCatalogError(
                f"{row_number}행의 정류장명이 비어 있습니다."
            )

        try:
            city_code = int((row.get("도시코드") or "").strip())
            gps_latitude = _optional_float(row.get("위도"))
            gps_longitude = _optional_float(row.get("경도"))
        except ValueError as exc:
            raise StationCatalogError(
                f"{row_number}행에 잘못된 숫자 값이 있습니다."
            ) from exc

        station_no = (row.get("모바일단축번호") or "").strip() or None
        return _StationRecord(
            station_id=station_id,
            station_name=station_name,
            station_no=station_no,
            gps_latitude=gps_latitude,
            gps_longitude=gps_longitude,
            city_code=city_code,
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
