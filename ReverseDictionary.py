from collections import defaultdict

class ReverseDictionary():

    #?PRIORITISE_WORDS_NEAR_TOP = True

    index_to_url_dic = {}

    #we can use this dic to weight the word counts
    index_to_num_words_dic = {}

    #this dic contains a word to a dictionary of url index to a list of the position of the word in the content
    #if we want to do pure bag of words we can just ignore the number of times info
    word_to_indices_dic = {}


    def build_dictionary(self, urls, contents):

        for url_index in range(0,len(urls)):
            one_url =  urls[url_index]
            one_content = contents[url_index]
            num_words = len(one_content)
            self.index_to_url_dic[url_index] = one_url
            self.index_to_num_words_dic[url_index] = num_words

            for i in range(num_words):
                word = one_content[i]
                if word in self.word_to_indices_dic:
                    word_dic = self.word_to_indices_dic[word]
                else:
                    word_dic = {}
                    self.word_to_indices_dic[word] = word_dic

                if not url_index in word_dic:
                    word_locations = []
                    word_dic[url_index] = word_locations
                else:
                    word_locations = word_dic[url_index]

                word_locations.append(i)

    #return dictionary of url to number of occurances of word
    def get_urls_one_word(self, word):

        all_url_indices_found = {}
        all_urls_found = {}

        if word in self.word_to_indices_dic:
            # dic of url index to number of occurances of word
            url_index_to_positions_dic = self.word_to_indices_dic[word]
            for url_index in url_index_to_positions_dic:
                all_url_indices_found[url_index] = len(url_index_to_positions_dic[url_index]) \
                                                   / self.index_to_num_words_dic[url_index]

        for url_index in all_url_indices_found:
            all_urls_found[self.index_to_url_dic[url_index]] = all_url_indices_found[url_index]

        return all_urls_found

    #1. return dictionary of url to words to positions
    def get_urls_multi_words(self, search_words):

        all_indices_found_word_positions = []
        all_urls_found = {}
        for word in search_words:
            if word in self.word_to_indices_dic:
                # dic of url index to number of occurances of word
                url_index_to_positions_dic = self.word_to_indices_dic[word]

                for url_index in url_index_to_positions_dic:
                    url = self.index_to_url_dic[url_index]
                    positions = url_index_to_positions_dic[url_index]

                    if not url in all_urls_found:
                        one_url_dic = {}
                        all_urls_found[url] = one_url_dic
                    else:
                        one_url_dic = all_urls_found[url]

                    one_url_dic[word] = positions

        return all_urls_found

    def get_urls(self, search_words):
        if len(search_words) == 1:
            return self.get_urls_one_word(search_words[0])
        else:
            return self.get_urls_multi_words(search_words)






