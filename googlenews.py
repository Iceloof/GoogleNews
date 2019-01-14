import bs4, sys
from bs4 import BeautifulSoup as soup
import urllib.request

class GoogleNews():

        def __init__(self):
                self.results = []
                self.results1 = []
                self.results2 = []

        def search(self, key, page=1):
                self.user_agent='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
                self.headers={'User-Agent':self.user_agent}
                self.url="https://www.google.com/search?q="+key+"&tbm=nws&start=%d" % (10*(page-1)) 
                self.req=urllib.request.Request(self.url, headers=self.headers)
                self.response=urllib.request.urlopen(self.req)
                self.page=self.response.read()
                self.content=soup(self.page, "html.parser")
                self.result=self.content.find(id="ires").find_all('h3')
                for item in self.result:
                        self.results.append(item.text)
                        self.results1.append(item.find('a').get('href'))
                        self.results2.append({'title':item.text,'link':item.find('a').get('href')})
                self.response.close()

        def get_result(self):
                return self.results2

        def get_result_text(self):
                return self.results

        def get_result_link(self):
                return self.results1

        def clear():
                self.results = []
                self.results1 = []
                self.results2 = []

