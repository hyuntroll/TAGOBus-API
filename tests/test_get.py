from tagoapi import *
from dotenv import load_dotenv
import os

import time 


load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = TAGOClient( auth=TAGOAuth(api_key) )

print(client.get_route_by_no(37400, "77")[0].to_dict())

start = time.time()


