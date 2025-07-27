from tagoapi import *
from dotenv import load_dotenv
import os

import time 


load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = TAGOClient( auth=TAGOAuth("FAKE_KEY") )

print(client.get_arrival_by_station(22, "23"))

start = time.time()