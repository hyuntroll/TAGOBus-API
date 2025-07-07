from tagoapi import *
import pickle
from pprint import pprint
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
# pprint(
#     get_city_code(api_key)
# )


## test decorater
class Universe:
    def __init__(self):
        pass

    @from_cache_or_fetch(2345)
    def testMethod(self, citycode: int, nodeId: int):
        print("method", citycode, nodeId)
        return "세마포어"

test1 = Universe()
print(test1.testMethod(citycode=12, nodeId=12))









""" test generating cache key 
client = TAGOClient(TAGOAuth("2345"))
print(
    client._from_cache_with_params("new", {"1":234, '4': 324})
)
"""
"""
data = {}
data[1] = {'no': 1, 'subject': '안2345녕 피클1', 'content': '피클은 매우 간단합니다.'}

with open('data.p', 'wb') as f:
    pickle.dump(data, f)


with open('data.p', 'rb') as f:
    print(pickle.load(f))

print(hash('adfk'))


client = TAGOClient(auth=TAGOAuth("3456"))

client._cache_save()

print(client._cache_get())
"""