import pickle
import sys

dic = pickle.load(open("page_rank_v5.p", "rb"))

full_parent_to_children_urls_dic = {}
i = 0
while i < 15:
    try:
        with open('../crawl-pr/data/parent_to_children_urls_{}.pickle'.format(i), 'rb') as handle:
            parent_to_children_urls_dic = pickle.load(handle)

        print("Adding in data for " + str(i))
        for key in parent_to_children_urls_dic:
            full_parent_to_children_urls_dic[key] = parent_to_children_urls_dic[key]

    except:
        print('nothing found for i: {}'.format(i))
    i += 1

for key in full_parent_to_children_urls_dic.keys():
    if 'meccano' in key:
        print(key)


