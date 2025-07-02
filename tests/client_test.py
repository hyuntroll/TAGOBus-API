from dotenv import load_dotenv
import os
from tagoapi import TAGOClient, get_city_code, get_station_by_keyword

load_dotenv()


def test_client():
    api_key = os.getenv('TAGO_API_KEY')
    client = TAGOClient(serviceKey=api_key)
    res1 = get_city_code(client)
    res2 = get_station_by_keyword(client, cityCode=22, keyword="민들레아파트")
    # print(res2)
    assert isinstance(res1, dict) # 응답이 dict이 맞는지 확인
    assert isinstance(res2, dict)
    # print(get_city_code(client))

# test_client()