import urllib.request

from bs4 import BeautifulSoup as Soup

class GoogleNews:

    def __init__(self,lang="en",period="",start="",end=""):
        self.__texts = []
        self.__links = []
        self.__results = []
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
        self.headers = {'User-Agent': self.user_agent}
        self.__lang = lang
        self.__period = period
        self.__start = start
        self.__end = end

    def setlang(self, lang):
        self.__lang = lang

    def setperiod(self, period):
        self.__period = period

    def setTimeRange(self, start, end):
        self.__start = start
        self.__end = end
        
    def search(self, key):
        """
        Searches for a term in google news and retrieves the first page into __results.
        
        Parameters:
        key = the search term
        """
        self.__key = "+".join(key.split(" "))
        self.getpage()

    def getpage(self, page=1):
        """
        Retrieves a specific page from google news into __results.

        Parameter:
        page = number of the page to be retrieved 
        """
        try:
            if self.__start != "" and self.__end != "":
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&tbs=lr:lang_1{},cdr:1,cd_min:{},cd_max:{}&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,self.__start,self.__end,(10 * (page - 1)))
            elif self.__period != "":
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&tbs=lr:lang_1{},qdr:{},&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,self.__period,(10 * (page - 1))) 
            else:
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&tbs=lr:lang_1{}&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,(10 * (page - 1))) 
        except AttributeError:
            raise AttributeError("You need to run a search() before using getpage().")
        try:
            self.req = urllib.request.Request(self.url, headers=self.headers)
            self.response = urllib.request.urlopen(self.req)
            self.page = self.response.read()
            self.content = Soup(self.page, "html.parser")
            result = self.content.find_all("div", id="search")[0].find_all("g-card")
            for item in result:
                try:
                    tmp_text = item.find("div", {"role" : "heading"}).text.replace("\n","")
                except Exception:
                    tmp_text = ''
                try:
                    tmp_link = item.find("a").get("href")
                except Exception:
                    tmp_link = ''
                try:
                    tmp_media = item.findAll("g-img")[1].parent.text
                except Exception:
                    tmp_media = ''
                try:
                    tmp_date = item.find("div", {"role" : "heading"}).next_sibling.findNext('div').findNext('div').text
                except Exception:
                    tmp_date = ''
                try:
                    tmp_desc = item.find("div", {"role" : "heading"}).next_sibling.findNext('div').text.replace("\n","")
                except Exception:
                    tmp_desc = ''
                try:
                    tmp_img = item.findAll("g-img")[0].find("img").get("src")
                except Exception:
                    tmp_img = ''
                self.__texts.append(tmp_text)
                self.__links.append(tmp_link)
                self.__results.append({'title': tmp_text, 'media': tmp_media,'date': tmp_date,'desc': tmp_desc, 'link': tmp_link,'img': tmp_img})
            self.response.close()
        except Exception:
            pass

    def get_news(self, deamplify=False):
        self.url = 'https://news.google.com/?hl={}'.format(self.__lang)
        try:
            self.req = urllib.request.Request(self.url, headers=self.headers)
            self.response = urllib.request.urlopen(self.req)
            self.page = self.response.read()
            self.content = Soup(self.page, "html.parser")
            self.content = self.content.find("h2").parent.parent.parent
            result = self.content.findChildren("div", recursive=False)
            section = None
            for item in result:
                try:
                    try:
                        section = item.find("h2").find("a").text
                    except Exception as sec_e:
                        pass
                    title = item.find("h3").text
                    if deamplify:
                        try:
                            link = item.find("article").get("jslog").split('2:')[1].split(';')[0]
                        except Exception as deamp_e:
                            print(deamp_e)
                            link = 'news.google.com/' + item.find("h3").find("a").get("href")
                    else:
                        link = item.find("h3").find("a").get("href")
                    self.__texts.append(title)
                    self.__links.append(link)
                    try:
                        datetime = item.find("time").get("datetime")
                    except:
                        datetime = None
                    try:
                        time = item.find("time").text
                    except:
                        time = None
                    try:
                        site = item.find("time").parent.find("a").text
                    except:
                        site = None
                    try:
                        img = item.find("img").get("src")
                    except:
                        img = None
                    desc = None
                    if link.startswith('https://www.youtube.com/watch?v='):
                        desc = 'video'

                    self.__results.append(
                        {'section': section,
                         'title': title,
                         'datetime': datetime,
                         'time': time,
                         'site': site,
                         'desc': desc,
                         'link': link,
                         'media': None,
                         'img': img})
                except Exception as big_e:
                    pass
            self.response.close()
        except Exception as e:
            print(e)
            pass

    def result(self):
        """Returns the __results."""
        return self.__results

    def gettext(self):
        """Returns only the __texts of the __results."""
        return self.__texts

    def get__links(self):
        """Returns only the __links of the __results."""
        return self.__links

    def clear(self):
        self.__texts = []
        self.__links = []
        self.__results = []
