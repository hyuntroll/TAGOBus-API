"""Non-blocking StationCatalog load and lookup benchmark."""

from statistics import mean
from time import perf_counter
import tracemalloc

from tagoapi import StationCatalog


def main() -> None:
    tracemalloc.start()
    catalog = StationCatalog()

    started_at = perf_counter()
    station_count = len(catalog)
    load_seconds = perf_counter() - started_at
    _, peak_bytes = tracemalloc.get_traced_memory()

    search_seconds = []
    for _ in range(20):
        started_at = perf_counter()
        catalog.search("중앙", limit=100)
        search_seconds.append(perf_counter() - started_at)

    print(f"stations={station_count}")
    print(f"initial_load_seconds={load_seconds:.4f}")
    print(f"average_search_seconds={mean(search_seconds):.6f}")
    print(f"peak_memory_mib={peak_bytes / 1024 / 1024:.2f}")


if __name__ == "__main__":
    main()
