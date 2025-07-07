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
@from_cache_or_fetch("www.example.com")
def test(citycode: int, nodeId: int, endpoint):
    
    print(citycode, nodeId, endpoint)
    return "뮤텍스락"
# print(test(citycode=2, nodeId=3456))


class universe:
    def __init__(self):
        pass

    @from_cache_or_fetch("www.example.com")
    def testMethod(self, citycode: int, nodeId: int, endpoint):
        print(citycode, nodeId, endpoint)
        return "세마포"

test1 = universe()
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