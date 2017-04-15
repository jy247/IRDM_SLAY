from PreProcess import PreProcess
from ReverseDictionary import ReverseDictionary
import pickle
import os

urls = []
urls.append('www.cat.com/index/')
urls.append('www.hat.com/find/something')
urls.append('www.run.com/find/something')

contents = []
contents.append('some story test about a cat cat')
contents.append('some story about a cat hat')
contents.append('running')


pp_obj = PreProcess()
for i in range(0, len(contents)):
    contents[i] = pp_obj.process_sentence(contents[i])

# rd_obj = ReverseDictionary()
# rd_obj.add_all(urls, contents)

print(os.getcwd())
i = 0
full_dic = ReverseDictionary()
full_parent_to_children_urls_dic = {}
try:
    while True:
        with open('./crawl-pr/data/Rdic_title_{}.pickle'.format(i), 'rb') as handle:
            titles_dic = pickle.load(handle)

        with open('./crawl-pr/data/parent_to_children_urls_{}.pickle'.format(i), 'rb') as handle:
            parent_to_children_urls_dic = pickle.load(handle)

        for key in parent_to_children_urls_dic:
            full_parent_to_children_urls_dic[key] = parent_to_children_urls_dic[key]

        new_dic = ReverseDictionary()
        new_dic.Decode(titles_dic)
        print('size of one dic: {}'.format(len(new_dic.index_to_url_dic)))
        full_dic.combine(new_dic)


        i += 1
except:
    print('loaded {} files'.format(i))
    print('size of full dic: {}'.format(len(full_dic.index_to_url_dic)))
    print('size of parent to child dic: {}'.format(len(full_parent_to_children_urls_dic)))




search_string = 'cat'
search_terms = pp_obj.process_sentence(search_string)
#
# print(rd_obj.get_urls(search_terms))