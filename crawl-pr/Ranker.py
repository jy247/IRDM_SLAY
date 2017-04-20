from ReverseDictionary import ReverseDictionary
from PreProcess import PreProcess
import numpy as np
import operator
import json

class Ranker():

    pp_obj = PreProcess()
    distance_for_related_words = 5

    def get_top_10(self, search_terms, weights, contents_rd, titles_rd, page_ranks):

        terms_list = self.pp_obj.process_sentence(search_terms)
        # if terms_list is str:
        #     terms_list = [terms_list]

        urls_to_positions_contents = contents_rd.get_urls(terms_list)
        urls_to_positions_titles = titles_rd.get_urls(terms_list)

        #additive
        #1. percentage of words found * w1
        #2. number of times a word is followed (within 5) by another word in the search string * w2
        #3. number of words in the title * w3
        #4. number of time word in the title followed by another * w4
        #5. number of words in the outlinks * w5

        # then multiply the overall score by pagerank

        num_urls_returned = len(urls_to_positions_contents)
        num_search_terms = len(terms_list)

        urls_to_scores = {}
        i = 0
        for url, word_to_positions_dic in urls_to_positions_contents.items():
            scores = [0,0,0,0,0]
            if num_search_terms > 1:
                scores[0] = len(word_to_positions_dic)
                scores[1] = self.count_correct_orders(terms_list, word_to_positions_dic)
            else:
                scores[0] = word_to_positions_dic
            urls_to_scores[url] = scores

        for url, word_to_positions_dic in urls_to_positions_titles.items():
            if url in urls_to_scores:
                scores = urls_to_scores[url]
            else:
                scores = [0,0,0,0,0]
                urls_to_scores[url] = scores
            if num_search_terms > 1:
                scores[2] = len(word_to_positions_dic)
                scores[3] = self.count_correct_orders(terms_list, word_to_positions_dic)
            else:
                scores[2] = word_to_positions_dic

        for index, url in contents_rd.index_to_url_dic.items():
            for term in terms_list:
                if url.find(term) > -1:
                    if url in urls_to_scores:
                        scores = urls_to_scores[url]
                    else:
                        scores = [0, 0, 0, 0, 0]
                        urls_to_scores[url] = scores
                    scores[4] += 1

        urls_to_sum_scores = {}
        for url, scores in urls_to_scores.items():
            if url in page_ranks:
                sum_score = np.dot(scores, weights)
                sum_score *= page_ranks[url]
                urls_to_sum_scores[url] = sum_score
            else:
                print('warn! URL not found in page ranks: {}'.format(url)  )


        #sort and return top 10
        sorted_x = sorted(urls_to_sum_scores.items(), key=operator.itemgetter(1), reverse=True)
        sorted_x = sorted_x[0:10]
        ret_urls_and_scores = []
        for url,_ in sorted_x:
            ret_urls_and_scores.append([url, urls_to_scores[url]])

        return json.dumps(ret_urls_and_scores)


    def count_correct_orders(self, search_terms, word_to_positions_dic):
        correct_orders = 0
        for i in range(len(search_terms)):
            first_word = search_terms[i]
            for j in range(i, len(search_terms)):
                second_word = search_terms[j]
                if first_word in word_to_positions_dic and second_word in word_to_positions_dic:
                    for first_pos in word_to_positions_dic[first_word]:
                        for second_pos in range(i, len(search_terms)):
                            diff = second_pos - first_pos
                            if abs(diff) <= self.distance_for_related_words:
                                correct_orders += 1
        return correct_orders







