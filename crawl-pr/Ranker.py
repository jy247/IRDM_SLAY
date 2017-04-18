from ReverseDictionary import ReverseDictionary
from PreProcess import PreProcess
import numpy as np
import operator


class Ranker():

    pp_obj = PreProcess()
    distance_for_related_words = 5

    def get_top_10(self, search_terms, contents_rd, titles_rd, parent_to_children_urls, page_ranks):

        terms_list = self.pp_obj.process_sentence(search_terms)
        urls_to_positions_contents = contents_rd.get_urls(search_terms)
        urls_to_positions_titles = titles_rd.get_urls(search_terms)

        #additive
        #1. percentage of words found * w1
        #2. number of times a word is followed (within 5) by another word in the search string * w2
        #3. number of words in the title * w3
        #4. number of time word in the title followed by another * w4
        #5. number of words in the outlinks * w5

        # then multiply the overall score by pagerank

        w1 = 1
        w2 = 1
        w3 = 1
        w4 = 1
        w5 = 1
        weights = np.transpose([ w1 , w2 ,w3 ,w4 ,w5])

        num_urls_returned = len(urls_to_positions_contents)
        num_search_terms = len(search_terms)

        urls_to_scores = {}
        i = 0
        for url, word_to_positions_dic in urls_to_positions_contents.items():
            scores = [0,0,0,0,0]
            scores[0] = len(word_to_positions_dic)
            if num_search_terms > 1:
                scores[1] = self.count_correct_orders(search_terms, word_to_positions_dic)
            urls_to_scores[url] = scores

        for url, word_to_positions_dic in urls_to_positions_contents.items():
            if url in urls_to_scores:
                scores = urls_to_scores[url]
            else:
                scores = [0,0,0,0,0]
                urls_to_scores[url] = scores
            scores[2] = len(word_to_positions_dic)
            if num_search_terms > 1:
                scores[3] = self.count_correct_orders(search_terms, word_to_positions_dic)

        for url, scores in urls_to_scores:
            if url in parent_to_children_urls:
                children_urls = parent_to_children_urls[url]
                for term in search_terms:
                    for child in children_urls:
                        if child.find(term) > -1:
                            scores[4] += 1

        for url, scores in urls_to_scores:
            if url in page_ranks:
                sum_score = np.dot(scores, weights)
                sum_score *= page_ranks[url]
            else:
                print('warn! URL not found in page ranks: {}'.format(url)  )


        #sort and return top 10
        sorted_x = sorted(urls_to_scores.items(), key=operator.itemgetter(1))
        return sorted_x[0:10]







    def count_correct_orders(self, search_terms, word_to_positions_dic):
        correct_orders = 0
        for i in range(len(search_terms)):
            first_word = search_terms[i]
            for j in range(i, len(search_terms)):
                second_word = search_terms[j]
                if first_word in word_to_positions_dic and second_word in word_to_positions_dic:
                    for first_pos in word_to_positions_dic[first_word]:
                        for second_pos in range(i, len(search_terms)):
                            diff = second_pos - first_word
                            if diff > 0 and diff <= self.distance_for_related_words:
                                correct_orders += 1
        return correct_orders







