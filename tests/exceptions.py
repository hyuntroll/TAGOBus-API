from tagoapi import *
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('TAGO_API_KEY')

client = TAGOClient(auth=TAGOAuth(api_key))

print(client.get_route_by_no(22, "32546"))