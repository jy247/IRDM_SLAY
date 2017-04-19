import pickle
import os

print(os.getcwd())

with open('./data/url_service.pickle', 'rb') as handle:
    urls = pickle.load(handle)

print(len(urls))
new_urls = []
for one_url,_ in urls.items():
    if one_url.find('www') > -1:
        new_urls.append(one_url)
    else:
        print(one_url)

print(len(new_urls))

