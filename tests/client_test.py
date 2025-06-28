from dotenv import load_dotenv
import os
from tagoapi import TAGOClient, get_city_code

load_dotenv()

def test_client():
    api_key = os.getenv('TAGO_API_KEY')
    client = TAGOClient(serviceKey=api_key)
    response = get_city_code(client)

    assert isinstance(response, dict) # 응답이 dict이 맞는지 확인
    # print(get_city_code(client))

# test_client()