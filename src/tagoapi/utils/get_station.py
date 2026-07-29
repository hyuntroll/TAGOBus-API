"""정류소 CSV 카탈로그 구현을 위한 데이터 규격 메모.

현재 공개 API는 제공하지 않는다. 추후 StationCatalog가 아래 공식 데이터
컬럼을 읽어 Station 모델로 변환한다.

- 정류장번호 -> station_id
- 정류장명 -> station_name
- 모바일단축번호 -> station_no
- 위도 -> gps_latitude
- 경도 -> gps_longitude
- 도시코드 -> city_code
"""
