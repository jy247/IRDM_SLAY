import random
import string
import cherrypy
import json
from collections import deque

class URLService(object):

    scanned_urls = {}
    queue = deque()
    NUM_PER_QUERY = 5
    unique_index = 0

    registered_crawlers = []
    breathing_crawlers = {}

    @cherrypy.expose
    def push(self, urls):
        #stupid dynamically type language
        if type(urls) is str:
            urls = [urls]

        for url in urls:

            if not url in self.scanned_urls:
                #we could easily keep track of which crawler has what data here
                self.scanned_urls[url] = self.unique_index
                self.unique_index += 1
                self.queue.append(url)
                #print('adding url: ' + url)

    @cherrypy.expose
    def pull(self, id):

        i = 0
        ret_urls = []
        while self.queue and i < self.NUM_PER_QUERY:
            url = self.queue.popleft()
            #print('dispensed:' + url)
            ret_urls.append([url, self.scanned_urls[url]])

            i += 1
            if not id in self.breathing_crawlers:
                self.breathing_crawlers[id] = 1
                print('Added Crawler! ID: {}'.format(id))

        if i == 0 and id in self.breathing_crawlers:
            self.breathing_crawlers.pop(id)
            print('Removed Crawler! ID: {}'.format(id))

        ret_json = json.dumps(ret_urls)
        return ret_json

    @cherrypy.expose
    def checkterminate(self):
        if len(self.breathing_crawlers) == 0:
            print('terminating!')
            return 'True'

        return 'False'

    @cherrypy.expose
    def reset(self):

        self.scanned_urls = {}
        self.queue = deque()
        self.breathing_crawlers = {}

    @cherrypy.expose
    def register(self):

        new_crawler_id = len(self.registered_crawlers)
        self.registered_crawlers.append(new_crawler_id)
        return str(new_crawler_id)

if __name__ == '__main__':
    cherrypy.quickstart(URLService())