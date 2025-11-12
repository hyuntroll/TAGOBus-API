from tagoapi import TAGOAuth, TAGOClient
from tagoapi.utils.cache import cache
from pprint import pprint
import time

import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.environ.get("TAGO_API_KEY")
client = TAGOClient(TAGOAuth(api_key))

# print(cache.current_cache)
# print(client.get_route_by_no(routeNo="북구", cityCode=22))
print(cache.current_cache)

route = client.get_route_by_no(routeNo="북구1", cityCode=22)

# pprint(cache.current_cache)
print(route[0].stations)

