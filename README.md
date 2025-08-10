# TAGOBus-API
[![Upload Python Package](https://github.com/hyuntroll/TAGOBus-API/actions/workflows/python-publish.yml/badge.svg)](https://github.com/hyuntroll/TAGOBus-API/actions/workflows/python-publish.yml)
![pypi version](https://img.shields.io/pypi/v/Unoffical-Tago-API) ![license](https://img.shields.io/github/license/hyuntroll/TAGOBus-API)

**TAGOBus-API**는 국가대중교통정보센터(TAGO)에서 제공하는 **버스 정보 API**를 Python에서 쉽게 사용할 수 있도록 만든 **비공식 Python 라이브러리**입니다.



## 설치

`Unoffical-TAGO-API` 는 python 3.10 이상의 버전을 지원합니다. (추후 3.10 이하 버전도 지원할 예정입니다.)

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

| 매개변수  | 설명 |
|-----------|------|
| `cityCode` | 도시 코드 |
| `routeNo`  | 버스 노선 번호 |
| `routeId`  | 버스 노선 ID |
| `nodeId`   | 정류소 ID |
| `nodeNm`   | 정류소 이름 |
| `nodeNo`   | 정류소 번호 |
| `gpsLati`  | 위도(WGS84) |
| `gpsLong`  | 경도(WGS84) |

---

## 사용 법

### 1. 클라이언트 생성

```python
from tagoapi import TAGOClient, TAGOAuth

client = TAGOClient(auth=TAGOAuth("YOUR_SERVICE_KEY"))
```
---

### 2. 정류장 검색 (로컬 함수)
클라이언트를 사용하지 않고도 **지역 기반 정류장 검색**이 가능합니다.

```python
from tagoapi import get_station

stations = get_station("대구")
print(stations)
```

---

### 3. 도메인 클래스

모든 메서드와 `get_station` 함수는 다음과 같은 **도메인 객체**를 반환합니다.

- `Station` : 정류소 정보  
- `Vehicle` : 버스 차량 정보  
- `Route` : 버스 노선 정보  
- `ArrivalInfo` : 버스 도착 정보

#### 공통 메서드
~~~python
obj.to_dict()             # 객체 → dict 변환
ClassName.from_dict(dict) # dict → 객체 변환
ClassName.from_list(list) # dict 리스트 → 객체 리스트 변환
~~~

---

### 도메인 객체 필드 목록

#### **Station**
| 필드명 | 타입 | 설명 |
|--------|------|------|
| `nodeId` | `str` | 정류소 ID |
| `nodeNm` | `str` | 정류소명 |
| `nodeNo` | `int` | 정류소 번호 |
| `gpsLati` | `float` | 위도 (WGS84) |
| `gpsLong` | `float` | 경도 (WGS84) |
| `cityCode` | `int` | 도시코드 |
| `updowncd` | `int` | 상하행구분코드 (`0`: 상행, `1`: 하행) |
| `nodeord` | `int` | 정류소순번 |

#### **Route**
| 필드명 | 타입 | 설명 |
|--------|------|------|
| `routeId` | `str` | 노선 ID |
| `routeNo` | `str` | 노선명 |
| `routeTp` | `int` | 노선유형 |
| `endNodeNm` | `str` | 종점 |
| `startNodeNm` | `str` | 기점 |
| `endvehicletime` | `int` | 막차시간 |
| `startvehicletime` | `int` | 첫차시간 |

#### **ArrivalInfo**
| 필드명 | 타입 | 설명 |
|--------|------|------|
| `nodeId` | `str` | 정류소 ID |
| `nodeNm` | `str` | 정류소명 |
| `routeId` | `str` | 노선 ID |
| `routeNo` | `str` | 노선명 |
| `routeTp` | `int` | 노선유형 |
| `arrprevstationcnt` | `int` | 노선유형 |
| `vehicletp` | `str` | 차랑유형 |
| `arrtime` | `int` | 도착예상시간 |

#### **Vehicle**
| 필드명 | 타입 | 설명 |
|--------|------|------|
| `routeId` | `str` | 노선 ID |
| `routeNo` | `str` | 노선명 |
| `gpsLati` | `float` | 위도 (WGS84) |
| `gpsLong` | `float` | 경도 (WGS84) |
| `arrtime` | `int` | 도착예상시간 |
| `arrprevstationcnt` | `int` | 노선유형 |
| `vehicleTp` | `str` | 차랑유형 |
| `vehicleNo` | `str` | 차랑번호 |



## 지원 API 목록

| 메서드 | 설명 | 매개변수 |
|--------|------|----------|
| `get_route_by_no` | 버스 노선 번호로 조회 | `cityCode`, `routeNo` |
| `get_route_by_id` | 노선 ID로 정보 조회 | `cityCode`, `routeId` |
| `get_route_by_station` | 정류소 경유 노선 조회 | `cityCode`, `nodeId` |
| `get_station_by_route` | 노선 경유 정류소 조회 | `cityCode`, `routeId` |
| `get_station` | 정류소명 또는 번호로 조회 | `cityCode`, `nodeNm` (선택: `nodeNo`) |
| `get_station_by_gps` | GPS 좌표 기반 주변 정류소 조회 | `gpsLati`, `gpsLong` |
| `get_arrival_by_station` | 실시간 도착예정정보 및 운행정보 목록을 조회 | `cityCode`, `nodeId` |
| `get_route_arrival_by_station` | 특정노선의 실시간 도착예정정보 및 운행정보 목록을 조회 | `cityCode`, `nodeId`, `routeId` |
| `get_route_pos` | 버스의 GPS위치정보의 목록을 조회 | `cityCode`, `routeId` |
| `get_route_pos_near_station` | 특정정류소에 접근한 버스의 GPS위치정보를 조회 | `cityCode`, `routeId`, `nodeId` |

---
### 5. 오류 및 이슈
버그 제보 또는 기능 요청은 [GitHub 이슈](https://github.com/hyuntroll/TAGOBus-API/issues)에 등록해주세요.