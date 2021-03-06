from collections import defaultdict
import re
import nltk


class PreProcess():

    regex = re.compile('[^a-zA-Z ]')
    stop_words = defaultdict()
    # stemmer = nltk.PorterStemmer()
   # tokenizer = nltk.LineTokenizer()

    with open("./stop_words.txt") as f:
        all_lines = f.read().splitlines()
        for line in all_lines:
            stop_words[line] = 0


    def remove_punc(self, sentence):
        return self.regex.sub('', sentence)

    def remove_stop_words(self, words):
        ret_query = []
        for word in words:
            if not word in self.stop_words:
                ret_query.append(word)
        return ret_query

    def process_data(self, data):
        if data is str:
            return self.process_sentence(data)
        else:
            one_array = []
            for sentence in data:
                one_array.extend(self.process_sentence(sentence))
            return one_array

    def process_sentence(self, sentence):
        punc_less = self.remove_punc(sentence)
        caps_less = punc_less.lower()
        # self.stemmer.stem(caps_less)
        words = nltk.word_tokenize(caps_less, 'english')
        #print(words)
        return self.remove_stop_words(words)







