
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tagoapi import *
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('TAGO_API_KEY')

print(get_station("민들"))

