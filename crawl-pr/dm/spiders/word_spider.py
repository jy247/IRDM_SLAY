import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from ..pagerank import powerIteration
import pickle
import json

# The command is scrapy crawl ucl.ac.uk -o output.json
# Simply install all dependencies and it runs like a normal python app

class WordSpider(scrapy.Spider):
    @classmethod
    # Where it all begins
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(WordSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        input("Press Enter to continue...")
        return spider

    # Signal Handler (similar to those in C) that intercepts spider_closed signal when crawling over
    def spider_closed(self, spider):
        ranks = powerIteration(self.get_matrix(), rsp=0.15, epsilon=0.00001, maxIterations=1000)
        pickle.dump(ranks, open("pagerank.p", "wb"))

    # Encapsulation for persistent objects
    def __init__(self):
        object.__init__(self)
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
        'https://assemblyseries.wustl.edu/'
    ]

    # Do not follow outlinks that are outside of the scope of the search engine
    allowed_domains = ['wustl.edu']

    # Once the page has been crawled, this function parses the data
    def parse(self, response):
        # url of current page
        url = response.url

        yield {
            'content': response.css('p::text').extract(),
            'title': response.css('title::text').extract(),
            'url' : url
        }

        extractor = LinkExtractor(allow_domains='assemblyseries.wustl.edu')
        links = extractor.extract_links(response)

        link_list = []
        for link in links:
            link_list.append(link)

        self.add_page(url, link_list)

        for link in links:
            yield scrapy.Request(link.url, callback=self.parse)
