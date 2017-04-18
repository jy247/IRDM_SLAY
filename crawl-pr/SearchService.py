import random
import pickle
import cherrypy
import json
from ReverseDictionary import ReverseDictionary
from PreProcess import PreProcess

class SearchService(object):

    full_dic = ReverseDictionary()
    full_parent_to_children_urls_dic = {}
    return_values = []

    i = 0
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

    @cherrypy.expose
    def search(self, search_terms):
        #stupid dynamically type language

        return_values = []

        self.full_dic.get_urls(search_terms)



if __name__ == '__main__':
    cherrypy.quickstart(SearchService())