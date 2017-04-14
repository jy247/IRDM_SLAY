# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from collections import defaultdict

class DmPipeline(object):

    collection_name = 'scrapy_items'
    regex = re.compile('[^a-zA-Z ]')
    stop_words = defaultdict()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(


        )

    def open_spider(self, spider):

        with open("../stop_words.txt") as f:
            all_lines = f.read().splitlines()
            for line in all_lines:
                self.stop_words[line] = 0



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

    def process_item(self, item, spider):
        item['content'] = self.process_sentence(' '.join(item['content']))
        return item
