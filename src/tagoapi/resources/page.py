from dataclasses import dataclass
from collections.abc import Iterator
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class TagoPage(Generic[T]):
    """TAGO 목록 응답과 페이지 메타데이터."""

    items: list[T]
    page_no: int
    num_of_rows: int
    total_count: int

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
