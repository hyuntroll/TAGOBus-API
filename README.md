# TAGOBus-API
[![Upload Python Package](https://github.com/hyuntroll/TAGOBus-API/actions/workflows/python-publish.yml/badge.svg)](https://github.com/hyuntroll/TAGOBus-API/actions/workflows/python-publish.yml)
![pypi version](https://img.shields.io/pypi/v/Unoffical-Tago-API) ![license](https://img.shields.io/github/license/hyuntroll/TAGOBus-API)

**TAGOBus-API**는 국가대중교통정보센터(TAGO)에서 제공하는 **버스 정보 API**를 Python에서 쉽게 사용할 수 있도록 만든 **비공식 Python 라이브러리**입니다.



## 설치

`Unoffical-TAGO-API`는 Python 3.10 이상을 지원합니다.

## 버전 정책

버전은 `MAJOR.MINOR.PATCH` 형식을 사용합니다.

- `MAJOR`: 하위 호환되지 않는 공개 API 변경
- `MINOR`: 하위 호환되는 기능 추가 및 deprecation
- `PATCH`: 하위 호환되는 버그 수정

현재 개발 버전은 `0.14.0`입니다. Deprecated Client 메서드와 기존 예외
alias는 `1.0.0`에서 제거할 예정입니다.

```bash
pip install Unoffical-TAGO-API
```

## 사용 전 준비사항

본 API를 사용하기 위해서는 **공공데이터포털**에서 TAGO 버스 관련 데이터를 활용 신청해야 합니다.

[국토교통부_(TAGO)_버스정류소정보](https://www.data.go.kr/data/15098534/openapi.do)

[국토교통부_(TAGO)_버스노선정보](https://www.data.go.kr/data/15098529/openapi.do)

[국토교통부_(TAGO)_버스도착정보](https://www.data.go.kr/data/15098530/openapi.do)

[국토교통부_(TAGO)_버스위치정보](https://www.data.go.kr/data/15098533/openapi.do)

**서비스 키**는 [공공데이터포털 마이페이지](https://www.data.go.kr/iim/main/mypageMain.do)에서 **Decoding 키**를 사용하세요.


## 주요 매개변수

라이브러리의 공개 API는 snake_case 매개변수를 사용합니다.

| 매개변수 | 설명 |
|---|---|
| `city_code` | 도시 코드 |
| `route_no` | 버스 노선 번호 |
| `route_id` | 버스 노선 ID |
| `station_id` | 정류소 ID |
| `station_name` | 정류소 이름 |
| `station_no` | 정류소 번호 |
| `gps_latitude` | 위도(WGS84) |
| `gps_longitude` | 경도(WGS84) |

---

## 사용법

### 1. 클라이언트 생성

```python
from tagoapi import TAGOClient

client = TAGOClient(service_key="YOUR_SERVICE_KEY")
```

### 2. 서비스 가능 도시 조회

```python
cities = client.cities.list()

for city in cities:
    print(city.city_code, city.city_name)
```

### 3. 노선과 정류소 조회

```python
routes = client.routes.list(city_code=22, route_no="북구1")

for route in routes:
    print(route.route_id, route.route_no)

stations = client.routes.list_stations(
    city_code=22,
    route_id=routes.items[0].route_id,
    num_of_rows=100,
)

print(stations.total_count)
for station in stations:
    print(station.station_id, station.station_name)
```

### 4. 오프라인 정류소 검색

`StationCatalog`는 패키지에 포함된 공식 정류소 스냅샷을 사용하므로 서비스
키나 네트워크 호출 없이 검색할 수 있습니다.

```python
from tagoapi import StationCatalog

catalog = StationCatalog()

stations = catalog.search("중앙역", city_code=25)
station = catalog.get("DJB8001793")
```

- `search(keyword, city_code=None, limit=100)`은 정류소 이름의 부분 일치
  결과를 원본 데이터 순서로 반환합니다.
- `limit=None`을 지정하면 일치하는 결과를 모두 반환합니다.
- `get(station_id)`은 정류소 ID가 없으면 `None`을 반환합니다.
- 데이터는 첫 조회 때 메모리에 읽히며 같은 인스턴스의 이후 조회에서
  재사용됩니다.

내장 데이터는 공공데이터포털의
[국토교통부_전국 버스정류장 위치정보](https://www.data.go.kr/data/15067528/fileData.do)
파일을 기반으로 합니다. 스냅샷 파일 기준일은 2025-06-15이고 CSV의
정보수집일은 2024-10-28입니다. 원본 데이터는 연간 갱신되므로 최신 변경이
즉시 반영되지 않을 수 있습니다.

목록 Resource는 `TagoPage`를 반환합니다.

```python
page.items        # 현재 페이지의 모델 목록
page.page_no      # 현재 페이지 번호
page.num_of_rows  # 요청한 페이지 크기
page.total_count  # 전체 결과 수
```

`TagoPage`는 반복과 `len()`을 지원하므로 모델 목록처럼 순회할 수 있습니다.

### 5. 도메인 클래스

클라이언트와 Resource는 다음과 같은 **도메인 객체**를 반환합니다.

- `CityCode`: 서비스 가능 도시
- `Station`: 정류소 정보
- `Vehicle`: 버스 차량 정보
- `Route`: 버스 노선 정보
- `ArrivalInfo`: 버스 도착 정보

## 도메인 객체 필드

### `BaseModel`

도메인 객체의 공통 상위 클래스이며 다음 메서드를 제공합니다.

```python
obj.to_dict()          # 객체 → dict 변환
Station.from_dict(raw) # TAGO 응답 dict → Station 변환
```

### `CityCode`

| 필드명 | 타입 | 설명 |
|---|---|---|
| `city_code` | `int` | 도시 코드 |
| `city_name` | `str` | 도시 이름 |

### `Station`

| 필드명 | 타입 | 설명 |
|---|---|---|
| `station_id` | `str` | 정류소 ID |
| `station_name` | `str` | 정류소 이름 |
| `station_no` | `str \| None` | 모바일 정류소 번호 |
| `gps_latitude` | `float \| None` | 위도 |
| `gps_longitude` | `float \| None` | 경도 |
| `city_code` | `int \| None` | 도시 코드 |
| `up_down_code` | `int \| None` | 상·하행 구분 코드 |
| `node_order` | `int \| None` | 노선 내 정류소 순서 |

### `Route`

| 필드명 | 타입 | 설명 |
|---|---|---|
| `route_id` | `str` | 노선 ID |
| `city_code` | `int \| None` | 도시 코드 |
| `route_no` | `str \| None` | 노선 번호 |
| `route_type` | `str \| None` | 노선 유형 |
| `start_node_name` | `str \| None` | 기점 |
| `end_node_name` | `str \| None` | 종점 |
| `start_vehicle_time` | `str \| None` | 첫차 시간 |
| `end_vehicle_time` | `str \| None` | 막차 시간 |
| `interval_time` | `int \| None` | 평일 배차 간격 |
| `interval_sat_time` | `int \| None` | 토요일 배차 간격 |
| `interval_sun_time` | `int \| None` | 일요일 배차 간격 |

### `ArrivalInfo`

| 필드명 | 타입 | 설명 |
|---|---|---|
| `station_id` | `str` | 정류소 ID |
| `route_id` | `str` | 노선 ID |
| `city_code` | `int \| None` | 도시 코드 |
| `station_no` | `str \| None` | 정류소 번호 |
| `station_name` | `str \| None` | 정류소 이름 |
| `route_no` | `str \| None` | 노선 번호 |
| `route_type` | `str \| None` | 노선 유형 |
| `previous_station_count` | `int \| None` | 남은 정류소 수 |
| `vehicle_type` | `str \| None` | 차량 유형 |
| `arrival_time` | `int \| None` | 도착 예상 시간(초) |

### `Vehicle`

| 필드명 | 타입 | 설명 |
|---|---|---|
| `route_id` | `str` | 노선 ID |
| `city_code` | `int \| None` | 도시 코드 |
| `route_no` | `str \| None` | 노선 번호 |
| `route_type` | `str \| None` | 노선 유형 |
| `station_id` | `str \| None` | 현재 정류소 ID |
| `station_name` | `str \| None` | 현재 정류소 이름 |
| `station_no` | `str \| None` | 현재 정류소 번호 |
| `node_order` | `int \| None` | 현재 정류소 순서 |
| `gps_latitude` | `float \| None` | 위도 |
| `gps_longitude` | `float \| None` | 경도 |
| `arrival_time` | `int \| None` | 도착 예상 시간(초) |
| `previous_station_count` | `int \| None` | 남은 정류소 수 |
| `vehicle_type` | `str \| None` | 차량 유형 |
| `vehicle_no` | `str \| None` | 차량 번호 |

## 지원 Resource API

| Resource 메서드 | 설명 |
|---|---|
| `client.cities.list()` | 서비스 가능 도시 조회 |
| `client.routes.list()` | 도시 및 노선번호로 노선 조회 |
| `client.routes.get()` | 노선 ID로 상세 조회 |
| `client.routes.list_stations()` | 노선 경유 정류소 조회 |
| `client.stations.list()` | 도시, 정류소명 또는 번호로 조회 |
| `client.stations.list_nearby()` | GPS 좌표 기반 주변 정류소 조회 |
| `client.stations.list_routes()` | 정류소 경유 노선 조회 |
| `client.arrivals.list_by_station()` | 정류소 도착예정정보 조회 |
| `client.arrivals.list_by_station_and_route()` | 정류소의 특정 노선 도착정보 조회 |
| `client.vehicles.list_by_route()` | 노선별 버스 위치 조회 |
| `client.vehicles.list_approaching_station()` | 특정 정류소 접근 버스 조회 |

기존 `client.get_route_by_no()` 등의 메서드는 호환성을 위해 유지되지만
`DeprecationWarning`을 발생시키며 1.0.0에서 제거될 예정입니다.

## 관계 데이터 조회

모델의 속성 접근은 네트워크 요청을 발생시키지 않습니다. 노선의 정류소나
정류소의 노선처럼 추가 조회가 필요한 데이터는 `client.routes`,
`client.stations` 등의 Resource 메서드를 명시적으로 호출해야 합니다.

## 예외 처리

```python
from tagoapi.exceptions import (
    RequestLimitExceededError,
    ServiceKeyNotRegisteredError,
    TagoAPIError,
)

try:
    cities = client.cities.list()
except ServiceKeyNotRegisteredError:
    print("서비스 키를 확인해주세요.")
except RequestLimitExceededError:
    print("요청 제한 횟수를 초과했습니다.")
except TagoAPIError as error:
    print(error)
```

## 개발 및 테스트

일반 테스트는 외부 네트워크를 사용하지 않습니다.

```bash
python -m pytest
```

실제 공공데이터 API 스모크 테스트는 명시적으로 활성화해야 합니다.
기본 검증 대상은 도시 코드 `25`, 노선 번호 `100`이며 환경변수로 변경할 수
있습니다.

```bash
TAGO_RUN_INTEGRATION=1 \
TAGO_API_KEY="YOUR_SERVICE_KEY" \
TAGO_TEST_CITY_CODE=25 \
TAGO_TEST_ROUTE_NO=100 \
python -m pytest -m integration tests/integration
```

---
### 오류 및 이슈
버그 제보 또는 기능 요청은 [GitHub 이슈](https://github.com/hyuntroll/TAGOBus-API/issues)에 등록해주세요.
