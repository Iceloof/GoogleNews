import urllib.request

from bs4 import BeautifulSoup as Soup


class GoogleNews:

    def __init__(self):
        self.texts = []
        self.links = []
        self.results = []
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
        self.headers = {'User-Agent': self.user_agent}

    def search(self, key):
        self.key = "+".join(key.split(" "))
        self.getpage()

    def getpage(self, page=1):
        self.url = "https://www.google.com/search?q=" + self.key + "&tbm=nws&start=%d" % (10 * (page - 1))
        try:
            self.req = urllib.request.Request(self.url, headers=self.headers)
            self.response = urllib.request.urlopen(self.req)
            self.page = self.response.read()
            self.content = Soup(self.page, "html.parser")
            result = self.content.find_all("div", class_="g")
            for item in result:
                self.texts.append(item.find("h3").text)
                self.links.append(item.find("h3").find("a").get("href"))
                self.results.append(
                    {'title': item.find("h3").text, 'media': item.find("div", class_="slp").find_all("span")[0].text,
                     'date': item.find("div", class_="slp").find_all("span")[2].text,
                     'desc': item.find("div", class_="st").text, 'link': item.find("h3").find("a").get("href"),
                     'img': item.find("img").get("src")})
            self.response.close()
        except Exception as e:
            print(e)
            pass

    def get_news(self, deamplify=False):
        self.url = 'https://news.google.com/'
        try:
            self.req = urllib.request.Request(self.url, headers=self.headers)
            self.response = urllib.request.urlopen(self.req)
            self.page = self.response.read()
            self.content = Soup(self.page, "html.parser")
            result = self.content.find_all("article")
            for item in result:
                try:
                    title = item.find("h3").text
                    if deamplify:
                        try:
                            link = item.find("a").get("jslog").split('2:')[1].split(';')[0]
                        except Exception as e:
                            print(e)
                            link = item.find("h3").find("a").get("href")
                    else:
                        link = item.find("h3").find("a").get("href")
                    self.texts.append(title)
                    self.links.append(link)
                    self.results.append(
                        {'title': title,
                         'datetime': item.find("time").get("datetime"),
                         'time': item.find("time").text,
                         'desc': item.find("h3").next_sibling.text,
                         'link': link,
                         'media': None,
                         'img': item.previous_sibling.find("img").get("src")})
                except Exception as e:
                    pass
            self.response.close()
        except Exception as e:
            print(e)
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
