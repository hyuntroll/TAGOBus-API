from tagoapi import TAGOAuth, TAGOClient
import pickle


data = {}
data[1] = {'no': 1, 'subject': '안2345녕 피클1', 'content': '피클은 매우 간단합니다.'}

# with open('data.p', 'wb') as f:
#     pickle.dump(data, f)


# with open('data.p', 'rb') as f:
#     print(pickle.load(f))

# print(hash('adfk'))


client = TAGOClient(auth=TAGOAuth("3456"))

# client._cache_save()

print(client._cache_get())