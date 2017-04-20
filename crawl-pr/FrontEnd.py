import random
import numpy as np
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
    def index(self, search_terms = '', w1=1, w2=1, w3=1, w4=1, w5=1):
        et = xml.etree.ElementTree.parse(self.index_file)
        root = et.getroot()
        if len(search_terms) != 0:
            weights = np.transpose([ w1 , w2 , w3 , w4 , w5])

            response = self.sesh.get(self.SearchService_Root + 'search/', params={'search_terms': search_terms,
                                                                                  'weights': weights})
            ret_urls = response.text
            i = 0
            for item in root.findall('body/ul/li'):
                item.text = ret_urls[i]

        return xml.etree.ElementTree.tostring(root)


        # with open('./index.html','r') as home_file:
        #     return home_file.read()


    # @cherrypy.expose
    # def search(self, search_terms):
    #     results = self.sesh.get(self.SearchService_Root + 'search/', params={'search_terms': search_terms})
    #     return results.text


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(FrontEnd())