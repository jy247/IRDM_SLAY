from collections import defaultdict

class ReverseDictionary():

    index_to_url_dic = {}

    #we can use this dic to weight the word counts
    index_to_num_words_dic = {}

    #this dic contains a word to a dictionary of url index to number of times the word appeared
    #if we want to do pure bag of words we can just ignore the number of times info
    word_to_indices_dic = {}


    def build_dictionary(self, urls, contents):

        for index in range(0,len(urls)):
            one_url =  urls[index]
            one_content = contents[index]
            self.index_to_url_dic[index] = one_url
            self.index_to_num_words_dic[index] = len(one_content)

            for word in one_content:
                if word in self.word_to_indices_dic:
                    word_dic = self.word_to_indices_dic[word]
                else:
                    word_dic = defaultdict(int)
                    self.word_to_indices_dic[word] = word_dic

                word_dic[index] += 1


    def get_urls(self, search_words):
        all_indices_found = defaultdict(float)
        all_urls_found = {}
        for word in search_words:
            if word in self.word_to_indices_dic:
                #dic of url index to number of occurances of word
                index_to_count_dic = self.word_to_indices_dic[word]
                for index in index_to_count_dic:
                    all_indices_found[index] += index_to_count_dic[index]

        for index in all_indices_found:
            all_urls_found[self.index_to_url_dic[index]] = all_indices_found[index]

        return all_urls_found



