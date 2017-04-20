import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from ..pagerank import powerIteration
import pickle
import json
import time
import os
import sys
from URLClient import URLClient
from collections import deque
from ReverseDictionary import ReverseDictionary
from PreProcess import PreProcess

# The command is scrapy crawl ucl.ac.uk -o output.json
# Simply install all dependencies and it runs like a normal python app

class WordSpider(scrapy.Spider):

    # This is the name of spider. When this is changed, so does the command to invoke the spider.
    name = "ucl.ac.uk"
    start_time = time.time()
    WRITE_OUTPUT = True
    write_interval = 1000
    data_folder = './data/'
    registration_id = 0
    pp_obj = PreProcess()

    # The URL from which to begin crawling
    start_urls = [
        'http://www.cs.ucl.ac.uk/home/'
    ]

    # Do not follow outlinks that are outside of the scope of the search engine
    allowed_domains = ['cs.ucl.ac.uk']

    #extractor = LinkExtractor(allow_domains='assemblyseries.wustl.edu')
    extractor = LinkExtractor(allow_domains='cs.ucl.ac.uk')
    queued_requests = deque()
    failures = []

    url_client = URLClient()
    WAIT_FOR_MORE_URLS = 10
    count = 0
    contents_dic = ReverseDictionary()
    titles_dic = ReverseDictionary()
    urls_ive_seen = {start_urls[0]: 0}
    parent_to_children_urls = {}
    #im starting to think scrapy is really unreliable
    # IGNORED_EXTENSIONS = [
    #     '7z', '7zip', 'xz', 'gz', 'tar', 'bz2', 'Z', 'tar.gz'  # archives
    #                                                  'cdr',  # Corel Draw files
    #     'apk',  # Android packages
    # ]

    @classmethod
    # Where it all begins
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(WordSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)

        return spider

    def save_output(self):

        encoded_contents = self.contents_dic.Encode()
        encoded_titles = self.titles_dic.Encode()

        with open(self.data_folder + 'parent_to_children_urls_{}.pickle'.format(self.registration_id), 'wb') as handle:
            pickle.dump(self.parent_to_children_urls, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(self.data_folder + 'Rdic_content_{}.pickle'.format(self.registration_id), 'wb') as handle:
            pickle.dump(encoded_contents, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open(self.data_folder + 'Rdic_title_{}.pickle'.format(self.registration_id), 'wb') as handle:
            pickle.dump(encoded_titles, handle, protocol=pickle.HIGHEST_PROTOCOL)


    # Signal Handler (similar to those in C) that intercepts spider_closed signal when crawling over
    def spider_closed(self, spider):
        #ranks = powerIteration(self.get_matrix(), rsp=0.15, epsilon=0.00001, maxIterations=1000)
        #pickle.dump(ranks, open("pagerank.p", "wb"))
        print('number of urls found: ' + str(len(self.urls_ive_seen)))
        time_taken = time.time() - self.start_time
        print('time take: {}'.format(time_taken))

        if self.WRITE_OUTPUT:
            self.save_output()


    # Encapsulation for persistent objects
    def __init__(self):
        object.__init__(self)
        self.start_time = time.time()
        self.page_rank = {}
        self.registration_id = self.url_client.Register()

    # Return the nested dictionary of link information
    def get_matrix(self):
        return self.page_rank

    # Once the page has been crawled, this function parses the data
    def parse(self, response):
        # url of current page
        # the request url is not necessarily the same as the response url.... that was a headache!
        #url = response.url
        try:
            # if response.url == 'http://www.financialcomputing.org/phd-programme/structure' :
            #     a = 0

            #print('response:' + str(response.status))
            the_url = response.url

            if not the_url in self.urls_ive_seen:
                self.urls_ive_seen[the_url] = 0

            #time.sleep(5)
            if response.status == 404:
                self.failures.append(the_url)
                return self.next_request()

            links = self.extractor.extract_links(response)

            #do the actual processing
            content = response.css('p::text').extract()
            title = response.css('title::text').extract()
            self.process_data(the_url, content, title)
            #print('processed!')

            #follow children
            #print('{} links found: '.format(len(links)))
            if len(links) != 0:
                self.parent_to_children_urls[the_url] = [l.url for l in links]
                #print('test links: ' + str(self.parent_to_children_urls[response.url]))
                new_links = []

                for link in links:
                    # if we were searching a larger domain we would have to come up with something more rigorous
                    if link.url.find('offset=') == -1 and link.url.find('oldid=') == -1:
                        if link.url not in self.urls_ive_seen:
                            self.urls_ive_seen[link.url] = 0
                            new_links.append(link.url)

                if len(new_links) > 0:
                    self.url_client.SendPushRequest(new_links)

            if self.WRITE_OUTPUT and len(self.parent_to_children_urls) % self.write_interval == 0:
                self.save_output()

            return self.next_request()
        except KeyError as err:
            print("Key error: {}".format(err))
            return self.next_request()
        except:
            print("Unexpected error:", sys.exc_info()[0])
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
                    #url to unique id

                    print('urls added: {}'.format(one_url))
                    self.urls_ive_seen[one_url] = 0
                    self.queued_requests.append(scrapy.Request(one_url, callback=self.parse, errback=self.parse, dont_filter=True))
                return self.queued_requests.popleft()
            else:
                time_to_die = self.url_client.CheckTermination()
                if time_to_die:
                    return None
                time.sleep(self.WAIT_FOR_MORE_URLS)

    def process_data(self, url, content, title):
        #print('test url: {}'.format(url))
        #print('test content: {}'.format(content))
        # unique_id = self.urls_ive_seen[url]

        processed_content = self.pp_obj.process_data(content)
        self.contents_dic.add_one(url, processed_content)

        processed_title = self.pp_obj.process_data(title)
        self.titles_dic.add_one(url, processed_title)
      #  print('processed content {}'.format(self.contents_dic.))


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
