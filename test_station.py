from tagoapi import *
import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("TAGO_API_KEY")
client = TAGOClient(TAGOAuth(key))

print(cache.current_cache)

print(client.get_station(22, nodeNm="삼덕"))

# print(get_station("대구소프트웨어마이스터고등학교"))
