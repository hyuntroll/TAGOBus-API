# Changelog

이 프로젝트는 `MAJOR.MINOR.PATCH` 버전 형식을 사용합니다.

## 0.14.0 - 2026-07-29

### Added

- 공식 정류소 데이터 기반 오프라인 `StationCatalog`
- `StationCatalogError`

### Changed

- 패키지 빌드 설정을 `pyproject.toml`로 전환

### Removed

- 구현되지 않은 `utils.get_station` 메모 모듈
- Resource와 연결되지 않던 실험적 model lazy-loading 기능

## 0.13.0 - 2026-07-29

### Added

- 서비스별 Route, Station, Arrival, Vehicle Resource
- `CityCode` 모델과 `CityResource`
- `TagoPage` 기반 페이지 응답

### Changed

- 모델과 Resource의 책임 분리
- 공공데이터포털 및 제공기관 예외 계층 정리
- 구형 Client 메서드를 deprecated API로 전환

### Removed

- `BaseList`
- pickle cache와 구형 converter/decorator
- requests 기반 구형 HTTP helper
