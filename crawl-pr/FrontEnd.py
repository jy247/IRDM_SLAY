import random
import string
import cherrypy
import json
import requests
import xml.etree.ElementTree

from collections import deque

class FrontEnd(object):

    SearchService_Root = 'http://127.0.0.1:8082/'
    index_file = './index.html'
    #lifecycle??
    sesh = requests.Session()

    @cherrypy.expose
    def index(self, search_terms = ''):
        et = xml.etree.ElementTree.parse(self.index_file)
        root = et.getroot()
        if len(search_terms) != 0:
            ret_urls = self.sesh.get(self.URLService_Root + 'search/', params={'search_terms': search_terms})
            i = 0
            for item in root.findall('body/ul/li'):
                item.text = ret_urls[i]

        return xml.etree.ElementTree.tostring(root)


        # with open('./index.html','r') as home_file:
        #     return home_file.read()

    @cherrypy.expose
    def search(self, search_terms):
        #results = self.sesh.get(self.SearchService_Root + 'search/', params={'search_terms': search_terms})
        return 'retval' #results.text


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(FrontEnd())