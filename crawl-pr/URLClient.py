import requests
import os
import json

class URLClient():

    #session lifecycle handling?
    sesh = requests.Session()
    pid = os.getpid()

    def SendPushRequest(self, urls):
        self.sesh.get('http://127.0.0.1:8080/push/', params={'urls': urls})

    def SendPullRequest(self):
        r = self.sesh.get('http://127.0.0.1:8080/pull/', params={'pid': self.pid})
        r = json.loads(r.text)
        if type(r) is str:
            return [r]
        else:
            return r

    def CheckTermination(self):
        r = self.sesh.get('http://127.0.0.1:8080/checkterminate/')
        return r

    def reset(self):
        r = self.sesh.reset('http://127.0.0.1:8080/reset/')

# test = URLClient()
#
# urls = ['www.test.com', 'www.cat.com']
# test.SendPushRequest(urls)
# r = test.SendPullRequest()
#
# r = test.CheckTermination()
# if bool(r):
#     print('yes')
# else:
#     print('no')