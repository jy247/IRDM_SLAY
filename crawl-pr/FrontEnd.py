import random
import string
import cherrypy
import json
from collections import deque

class FrontEnd(object):

    scanned_urls = {}
    queue = deque()
    NUM_PER_QUERY = 5
    unique_index = 0

    registered_crawlers = []
    breathing_crawlers = {}



    @cherrypy.expose
    def search(self):

        self.scanned_urls = {}
        self.queue = deque()
        self.breathing_crawlers = {}


if __name__ == '__main__':
    cherrypy.quickstart(URLService())