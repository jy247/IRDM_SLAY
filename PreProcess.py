from collections import defaultdict
import re


class PreProcess():

    regex = re.compile('[^a-zA-Z ]')
    stop_words = defaultdict()

    with open("stop_words.txt") as f:
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


    def process_sentence(self, sentence):
        words = str.split(str.lower(self.remove_punc(sentence)), ' ')
        return self.remove_stop_words(words)







