import pickle
import sys

dic = pickle.load(open("page_rank_v5.p", "rb"))

set = set()

print(len(dic.keys()))

for key in dic.keys():
    set.add(dic[key])


print(dic['http://www.cs.ucl.ac.uk/home/'])
