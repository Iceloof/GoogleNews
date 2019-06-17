from bs4 import BeautifulSoup as soup
import urllib.request

class GoogleNews():

        def __init__(self):
                self.texts = []
                self.links = []
                self.results = []

        def search(self, key):
                self.key = "+".join(key.split(" "))
                self.getpage()

        def getpage(self, page=1):
                self.user_agent='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
                self.headers={'User-Agent':self.user_agent}
                self.url="https://www.google.com/search?q="+self.key+"&tbm=nws&start=%d" % (10*(page-1)) 
                try:
                        self.req=urllib.request.Request(self.url, headers=self.headers)
                        self.response=urllib.request.urlopen(self.req)
                        self.page=self.response.read()
                        self.content=soup(self.page, "html.parser")
                        result=self.content.find(id="ires").find_all("div", class_="g")
                        for item in result:
                                self.texts.append(item.find("h3").text)
                                self.links.append(item.find("h3").find("a").get("href"))
                                self.results.append({'title':item.find("h3").text,'media':item.find("div", class_="slp").find_all("span")[0].text,'date':item.find("div", class_="slp").find_all("span")[2].text,'desc':item.find("div", class_="st").text,'link':item.find("h3").find("a").get("href"),'img':item.find("img").get("src")})
                        self.response.close()
                except Exception:
                        pass

        def result(self):
                return self.results

        def gettext(self):
                return self.texts

        def getlinks(self):
                return self.links

        def clear(self):
                self.texts = []
                self.links = []
                self.results = []
