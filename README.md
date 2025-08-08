# TAGOBus-API
[![Upload Python Package](https://github.com/hyuntroll/TAGOBus-API/actions/workflows/python-publish.yml/badge.svg)](https://github.com/hyuntroll/TAGOBus-API/actions/workflows/python-publish.yml)
![pypi version](https://img.shields.io/pypi/v/Unoffical-Tago-API) ![license](https://img.shields.io/github/license/hyuntroll/TAGOBus-API)

TAGOAPI는 국가대중교통정보센터(TAGO)에서 제공하는 버스 api를 파이썬에서 사용할 수 있게 만든 비공식 API입니다.


## 설치

`Unoffical-TAGO-API` 는 python 3.10 이상의 버전을 지원합니다. (추후 3.10 이하 버전도 지원할 예정입니다.)

```bash
pip install Unoffical-TAGO-API
```

## 사용 전 알아야 하는 사항

사용 전 

[국토교통부_(TAGO)_버스정류소정보](https://www.data.go.kr/data/15098534/openapi.do)

[국토교통부_(TAGO)_버스노선정보](https://www.data.go.kr/data/15098529/openapi.do)

[국토교통부_(TAGO)_버스도착정보](https://www.data.go.kr/data/15098530/openapi.do)

[국토교통부_(TAGO)_버스위치정보](https://www.data.go.kr/data/15098533/openapi.do)

에서 모두 데이터 활용 신청을 해야 합니다. (활용 신청을 하지 않으면 서비스를 이용하실 수 없습니다.)

서비스 키는 [공공 데이터 포털 마이 페이지](https://www.data.go.kr/iim/main/mypageMain.do) 에서 확인하실 수 있고, Decoding키를 사용합니다.

## 사용 법

### 1. Client 생성

TAGOClient를 통해 클라이언트를 만들 수 있습니다.

```python
from tagoapi import TAGOClient
from tagoapi import TAGOAuth

client = TAGClient(auth=TAGOAuth(YOUR_SERVICE_KEY))

```

### 2. 정류장 찾기_로컬

client를 사용하지 않고 정류장을 찾는 함수 입니다.

```python
from tagoapi import get_station

print( get_station("대구") )

```

### 3. 도메인 클래스

모든 메서드와 get_station함수는 리턴 값으로 `Station`, `Vehicle`, `Route`, `ArrivalInfo` 도메인 클래스를 가집니다.

도메인 클래스는 공통적으로 

```python
def to_dict(self): # 도메인 객체를 딕셔너리로 변환합니다. 

@classmethod
def from_dict(cls, data:dict):  # 딕셔너리를 도메인 객체로 변환합니다.

@classmethod
def from_list(cls, data:list): # 딕셔너리를 요소로 가진 리스트를 도메인 객체로 변환합니다.
```

메서드를 가지고 있습니다.

#### 3-1. Station
정류장 정보를 가지는 도메인 클래스 입니다.

#### 3-2. Vehicle
노선의 차량 정보를 가지는 도메인 클래스 입니다.

#### 3-3. Route
노선 정보를 가지는 도메인 클래스 입니다.

#### 3-4. ArrivalInfo
노선의 도착 정보를 가지는 도메인 클래스 입니다.


### 4. 오류 