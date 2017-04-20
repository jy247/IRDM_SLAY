import pickle
import os
import json
import requests

print(os.getcwd())
sesh = requests.session()

SearchService_Root = 'http://127.0.0.1:8082/'
search_terms = 'cat'
weights = ['0.5','0.5','0.5','0.5','0.5']

response = sesh.get(SearchService_Root + 'search/', params={'search_terms': search_terms, 'weights': weights})
val = json.loads(response.text)
print(json.loads(response.text))

# with open('./data/url_service.pickle', 'rb') as handle:
#     urls = pickle.load(handle)
#
# print(len(urls))
# new_urls = []
# for one_url,_ in urls.items():
#     if one_url.find('www') > -1:
#         new_urls.append(one_url)
#     else:
#         print(one_url)
#
# print(len(new_urls))

