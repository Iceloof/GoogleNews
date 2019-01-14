import bs4, sys
from bs4 import BeautifulSoup as soup
import urllib.request
from inscriptis import get_text

class GoogleNews():

        def __init__(self):
                self.results = []

        def search(self, key):
                self.user_agent='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
                self.headers={'User-Agent':self.user_agent}
                self.url="https://www.google.com/search?q="+key+"&tbm=nws"
                self.req=urllib.request.Request(self.url, headers=self.headers)
                self.response=urllib.request.urlopen(self.req)
                self.page=self.response.read()
                self.content=soup(self.page, "html.parser")
                self.result=self.content.find(id="ires").find_all('h3')
                for item in self.result:
                        self.results.append(item.text)
                self.url="https://www.google.com/search?q="+key+"&tbm=nws&start=10"
                self.req=urllib.request.Request(self.url, headers=self.headers)
                self.response=urllib.request.urlopen(self.req)
                self.page=self.response.read()
                self.content=soup(self.page, "html.parser")
                self.result=self.content.find(id="ires").find_all('h3')
                for item in self.result:
                        self.results.append(item.text)
                self.response.close()

        def get_result(self):
                return self.results


