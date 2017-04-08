import pickle
from operator import itemgetter
from collections import OrderedDict

result = pickle.load(open("pagerank.p", "rb"), encoding='latin1')

print(result)

def rankPages(listOfURLs):
    dict_selected_pages = {}

    for url in listOfURLs:
        dict_selected_pages[url] = result[url];

    return OrderedDict(sorted(dict_selected_pages.items(), key=itemgetter(1)))


