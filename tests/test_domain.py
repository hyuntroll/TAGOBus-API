import tagoapi
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = tagoapi.TAGOClient(tagoapi.TAGOAuth(api_key))

start = time.time()
lst = client.get_route_by_no(cityCode=22, routeNo="1")
end = time.time()
print(f"{end - start:.5f} sec")
print(lst)
