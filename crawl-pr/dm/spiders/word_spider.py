import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from ..pagerank import powerIteration
import pickle
import json
import time
import os
from URLClient import URLClient
from collections import deque

# The command is scrapy crawl ucl.ac.uk -o output.json
# Simply install all dependencies and it runs like a normal python app

class WordSpider(scrapy.Spider):

    start_time = time.time()
    url_client = URLClient()
    WAIT_FOR_MORE_URLS = 10
    count = 0

    @classmethod
    # Where it all begins
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(WordSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        #input("Press Enter to continue...")
        return spider

    # Signal Handler (similar to those in C) that intercepts spider_closed signal when crawling over
    def spider_closed(self, spider):
        #ranks = powerIteration(self.get_matrix(), rsp=0.15, epsilon=0.00001, maxIterations=1000)
        #pickle.dump(ranks, open("pagerank.p", "wb"))
        print('number of urls found: ' + str(len(self.urls_ive_seen)))
        time_taken = time.time() - self.start_time
        print('time take: {}'.format(time_taken))
        with open('ucl_all_urls_{}.txt'.format(os.getpid()), 'w') as f:
            f.writelines([ l for l in self.urls_ive_seen ])

        with open('ucl_all_urls_{}.pickle'.format(os.getpid()), 'wb') as handle:
            pickle.dump(self.urls_ive_seen, handle, protocol=pickle.HIGHEST_PROTOCOL)



    # Encapsulation for persistent objects
    def __init__(self):
        object.__init__(self)
        self.start_time = time.time()
        self.page_rank = {}

    # Add page and its outlinks to the page rank matrix (nested dictionary)
    def add_page(self, url, out_links):
        self.page_rank[url] = {}
        for link in out_links:
            self.page_rank[url][link.url] = 1

    # Return the nested dictionary of link information
    def get_matrix(self):
        return self.page_rank

    # This is the name of spider. When this is changed, so does the command to invoke the spider.
    name = "ucl.ac.uk"

    # The URL from which to begin crawling
    start_urls = [
        'http://www.cs.ucl.ac.uk/home/'
    ]

    # Do not follow outlinks that are outside of the scope of the search engine
    allowed_domains = ['cs.ucl.ac.uk']

    urls_ive_seen = {}
    #extractor = LinkExtractor(allow_domains='assemblyseries.wustl.edu')
    extractor = LinkExtractor(allow_domains='cs.ucl.ac.uk')
    queued_requests = deque()
    failures = []

    # Once the page has been crawled, this function parses the data
    def parse(self, response):
        # url of current page
        #url = response.url
        try:
            print('response:' + str(response.status))
            if response.status == 404:
                self.failures.append(response.url)
                return self.next_request()

            self.count += 1
            links = self.extractor.extract_links(response)
            #do the actual processing

            #follow children
            print('{} links found: '.format(len(links)))
            if len(links) != 0:
                new_links = []
                for link in links:
                    if link.url.find('offset=') == -1:
                        if link.url not in self.urls_ive_seen:
                            self.urls_ive_seen[link.url] = 0
                            new_links.append(link.url)

                if len(new_links) > 0:
                    self.url_client.SendPushRequest(new_links)

            return self.next_request()
        except:
            print('Error caught: ')
            return self.next_request()

    def next_request(self):

        if self.queued_requests:
            return self.queued_requests.popleft()

        time_to_die = False
        while not time_to_die:
            new_urls = self.url_client.SendPullRequest()
            #print('request received: ' + str(new_urls))
            if len(new_urls) > 0:
                for one_url in new_urls:
                    self.queued_requests.append(scrapy.Request(one_url, callback=self.parse, errback=self.parse))

                return self.queued_requests.popleft()
            else:
                time_to_die = self.url_client.CheckTermination()
                if time_to_die:
                    return None
                time.sleep(self.WAIT_FOR_MORE_URLS)


    # # Once the page has been crawled, this function parses the data
    # def parse(self, response):
    #     # url of current page
    #     url = response.url
    #
    #     yield {
    #         'content': response.css('p::text').extract(),
    #         'title': response.css('title::text').extract(),
    #         'url' : url
    #     }
    #
    #     extractor = LinkExtractor(allow_domains='assemblyseries.wustl.edu')
    #     links = extractor.extract_links(response)
    #
    #     link_list = []
    #     for link in links:
    #         link_list.append(link)
    #
    #     self.add_page(url, link_list)
    #
    #     for link in links:
    #         yield scrapy.Request(link.url, callback=self.parse)
