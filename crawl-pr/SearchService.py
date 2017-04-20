import random
import pickle
import cherrypy
import json
from ReverseDictionary import ReverseDictionary
from PreProcess import PreProcess
from cherrypy._cpserver import Server
from Ranker import Ranker

class SearchService(object):

    titles_dic = ReverseDictionary()
    contents_dic = ReverseDictionary()
    parent_to_children_urls_dic = {}
    return_values = []
    rank_engine = Ranker()
    data_root = './data/'

    i =0
    one_titles_dic = ReverseDictionary()
    one_contents_dic = ReverseDictionary()
    # one_parent_to_children_urls_dic = {}

    while i < 15:
        try:
            with open(data_root + 'Rdic_title_{}.pickle'.format(i), 'rb') as handle:
                one_titles_dic = pickle.load(handle)

            with open(data_root + 'Rdic_content_{}.pickle'.format(i), 'rb') as handle:
                one_contents_dic = pickle.load(handle)

            # with open(data_root + 'parent_to_children_urls_{}.pickle'.format(i), 'rb') as handle:
            #     one_parent_to_children_urls_dic = pickle.load(handle)
            #
            # for key in one_parent_to_children_urls_dic:
            #     parent_to_children_urls_dic[key] = one_parent_to_children_urls_dic[key]

            new_dic_titles = ReverseDictionary()
            new_dic_titles.Decode(one_titles_dic)
            print('size of one dic: {}'.format(len(new_dic_titles.index_to_url_dic)))
            titles_dic.combine(new_dic_titles)

            new_dic_contents = ReverseDictionary()
            new_dic_contents.Decode(one_contents_dic)
            contents_dic.combine(new_dic_contents)
        except:
            print('nothing found for i: {}'.format(i))

        i += 1

    print('loaded {} files'.format(i))
    print('size of full dic: {}'.format(len(titles_dic.index_to_url_dic)))
    #print('size of parent to child dic: {}'.format(len(parent_to_children_urls_dic)))

    #load page ranks
    page_ranks = json.loads(data_root + 'page_ranks.json')

    @cherrypy.expose
    def search(self, search_terms, weights):

        weight_as_numbers = []
        for one_weight in weights:
            weight_as_numbers.append(float(one_weight))
        return self.rank_engine.get_top_10(search_terms, weight_as_numbers, self.contents_dic, self.titles_dic, self.page_ranks)

if __name__ == '__main__':

    cherrypy.config.update({'server.socket_port': 8082})
    cherrypy.quickstart(SearchService())