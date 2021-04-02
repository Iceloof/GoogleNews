
### MODULES
import re
import urllib.request
import dateparser, copy
from bs4 import BeautifulSoup as Soup, ResultSet
from dateutil.parser import parse

import datetime
from dateutil.relativedelta import relativedelta

### METHODS

def lexical_date_parser(date_to_check):
    if date_to_check=='':
        return ('',None)
    datetime_tmp=None
    date_tmp=copy.copy(date_to_check)
    count=0
    while datetime_tmp==None and count <= (len(date_to_check)-3):
        datetime_tmp=dateparser.parse(date_tmp)
        if datetime_tmp==None:
            date_tmp=date_tmp[1:]
        count+=1

    if datetime_tmp==None:
        date_tmp=date_to_check
    else:
        datetime_tmp=datetime_tmp.replace(tzinfo=None)

    if date_tmp[0]==' ':
        date_tmp=date_tmp[1:]
    return date_tmp,datetime_tmp


def define_date(date):
    months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    try:
        if ' ago' in date.lower():
            q = int(date.split()[-3])
            if 'hour' in date.lower():
                return datetime.datetime.now() + relativedelta(hours=-q)
            elif 'day' in date.lower():
                return datetime.datetime.now() + relativedelta(days=-q)
            elif 'week' in date.lower():
                return datetime.datetime.now() + relativedelta(days=-7*q)
            elif 'month' in date.lower():
                return datetime.datetime.now() + relativedelta(months=-q)
        else:
            for month in months.keys():
                if month.lower()+' ' in date.lower():
                    date_list = date.replace(',','').split()[-3:]
                    return datetime.datetime(day=int(date_list[1]), month=months[month], year=int(date_list[2]))
    except:
        return float('nan')


### CLASSEs

class GoogleNews:

    def __init__(self,lang="en",period="",start="",end="",encode="utf-8"):
        self.__texts = []
        self.__links = []
        self.__results = []
        self.__totalcount = 0
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
        self.headers = {'User-Agent': self.user_agent}
        self.__lang = lang
        self.__period = period
        self.__start = start
        self.__end = end
        self.__encode = encode

    def set_lang(self, lang):
        self.__lang = lang

    def setlang(self, lang):
        """Don't remove this, will affect old version user when upgrade"""
        self.set_lang(lang)

    def set_period(self, period):
        self.__period = period

    def setperiod(self, period):
        """Don't remove this, will affect old version user when upgrade"""
        self.set_period(period)

    def set_time_range(self, start, end):
        self.__start = start
        self.__end = end

    def setTimeRange(self, start, end):
        """Don't remove this, will affect old version user when upgrade"""
        self.set_time_range(start, end)

    def set_encode(self, encode):
        self.__encode = encode

    def setencode(self, encode):
        """Don't remove this, will affect old version user when upgrade"""
        self.set_encode(encode)

    def search(self, key):
        """
        Searches for a term in google.com in the news section and retrieves the first page into __results.
        Parameters:
        key = the search term
        """
        self.__key = "+".join(key.split(" "))
        if self.__encode != "":
            self.__key = urllib.request.quote(self.__key.encode(self.__encode))
        self.get_page()

    def build_response(self):
        self.req = urllib.request.Request(self.url.replace("search?","search?hl=en&gl=en&"), headers=self.headers)
        self.response = urllib.request.urlopen(self.req)
        self.page = self.response.read()
        self.content = Soup(self.page, "html.parser")
        stats = self.content.find_all("div", id="result-stats")
        if stats and isinstance(stats, ResultSet):
            stats = re.search(r'\d+', stats[0].text)
            self.__totalcount = int(stats.group())
        else:
            #TODO might want to add output for user to know no data was found
            return
        result = self.content.find_all("div", id="search")[0].find_all("g-card")
        return result

    def page_at(self, page=1):
        """
        Retrieves a specific page from google.com in the news sections into __results.

        Parameter:
        page = number of the page to be retrieved
        """
        results = []
        try:
            if self.__start != "" and self.__end != "":
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&biw=1920&bih=976&source=lnt&&tbs=lr:lang_1{},cdr:1,cd_min:{},cd_max:{},sbd:1&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,self.__start,self.__end,(10 * (page - 1)))
            elif self.__period != "":
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&biw=1920&bih=976&source=lnt&&tbs=lr:lang_1{},qdr:{},,sbd:1&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,self.__period,(10 * (page - 1))) 
            else:
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&biw=1920&bih=976&source=lnt&&tbs=lr:lang_1{},sbd:1&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,(10 * (page - 1))) 
        except AttributeError:
            raise AttributeError("You need to run a search() before using get_page().")
        try:
            result = self.build_response()
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
                    tmp_date,tmp_datetime=lexical_date_parser(tmp_date)
                except Exception:
                    tmp_date = ''
                    tmp_datetime=None
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
                results.append({'title': tmp_text, 'media': tmp_media,'date': tmp_date,'datetime':define_date(tmp_date),'desc': tmp_desc, 'link': tmp_link,'img': tmp_img})
            self.response.close()
        except Exception as e_parser:
            print(e_parser)
            pass
        return results

    def get_page(self, page=1):
        """
        Retrieves a specific page from google.com in the news sections into __results.

        Parameter:
        page = number of the page to be retrieved 
        """
        try:
            if self.__start != "" and self.__end != "":
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&biw=1920&bih=976&source=lnt&&tbs=lr:lang_1{},cdr:1,cd_min:{},cd_max:{},sbd:1&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,self.__start,self.__end,(10 * (page - 1)))
            elif self.__period != "":
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&biw=1920&bih=976&source=lnt&&tbs=lr:lang_1{},qdr:{},,sbd:1&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,self.__period,(10 * (page - 1))) 
            else:
                self.url = "https://www.google.com/search?q={}&lr=lang_{}&biw=1920&bih=976&source=lnt&&tbs=lr:lang_1{},sbd:1&tbm=nws&start={}".format(self.__key,self.__lang,self.__lang,(10 * (page - 1))) 
        except AttributeError:
            raise AttributeError("You need to run a search() before using get_page().")
        try:
            result = self.build_response()
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
                    tmp_date,tmp_datetime=lexical_date_parser(tmp_date)
                except Exception:
                    tmp_date = ''
                    tmp_datetime=None
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
                self.__results.append({'title': tmp_text, 'media': tmp_media,'date': tmp_date,'datetime':define_date(tmp_date),'desc': tmp_desc, 'link': tmp_link,'img': tmp_img})
            self.response.close()
        except Exception as e_parser:
            print(e_parser)
            pass

    def getpage(self, page=1):
        """Don't remove this, will affect old version user when upgrade"""
        self.get_page(page)

    def get_news(self, key="",deamplify=False):
        if key != '':
            key = "+".join(key.split(" "))
            if self.__encode != "":
                key = urllib.request.quote(key.encode(self.__encode))
            self.url = 'https://news.google.com/search?q={}+when:{}&hl={}'.format(key,self.__period,self.__lang.lower())
        else:
            self.url = 'https://news.google.com/?hl={}'.format(self.__lang)
        try:
            self.req = urllib.request.Request(self.url, headers=self.headers)
            self.response = urllib.request.urlopen(self.req)
            self.page = self.response.read()
            self.content = Soup(self.page, "html.parser")
            articles = self.content.select('div[class="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"]')
            for article in articles:
                try:
                    # title
                    try:
                        title=article.find('h3').text
                    except:
                        title=None
                    # description
                    try:
                        desc=article.find('span').text
                    except:
                        desc=None
                    # date
                    try:
                        date = article.find("time").text
                        # date,datetime_tmp = lexial_date_parser(date)
                    except:
                        date = None
                    # datetime
                    try:
                        datetime_chars=article.find('time').get('datetime')
                        datetime_obj = parse(datetime_chars).replace(tzinfo=None)
                    except:
                        datetime_obj=None
                    # link
                    if deamplify:
                        try:
                            link = 'news.google.com/' + article.find("h3").find("a").get("href")
                        except Exception as deamp_e:
                            print(deamp_e)
                            link = article.find("article").get("jslog").split('2:')[1].split(';')[0]
                    else:
                            link = 'news.google.com/' + article.find("h3").find("a").get("href")
                    self.__texts.append(title)
                    self.__links.append(link)
                    if link.startswith('https://www.youtube.com/watch?v='):
                        desc = 'video'
                    # image
                    try:
                        img = article.find("img").get("src")
                    except:
                        img = None
                    # site
                    try:
                        site=article.find("time").parent.find("a").text
                    except:
                        site=None
                    # collection
                    self.__results.append({'title':title,
                                           'desc':desc,
                                           'date':date,
                                           'datetime':define_date(date),
                                           'link':link,
                                           'img':img,
                                           'media':None,
                                           'site':site})
                except Exception as e_article:
                    print(e_article)
            self.response.close()
        except Exception as e_parser:
            print(e_parser)
            pass

    def total_count(self):
        return self.__totalcount

    def result(self,sort=False):
        """Don't remove this, will affect old version user when upgrade"""
        return self.results(sort)

    def results(self,sort=False):
        """Returns the __results.
        New feature: include datatime and sort the articles in decreasing order"""
        results=self.__results
        if sort:
            try:
                results.sort(key = lambda x:x['datetime'],reverse=True)
            except Exception as e_sort:
                print(e_sort)
                results=self.__results
        return results

    def get_texts(self):
        """Returns only the __texts of the __results."""
        return self.__texts

    def gettext(self):
        """Don't remove this, will affect old version user when upgrade"""
        return self.get_texts()

    def get_links(self):
        """Returns only the __links of the __results."""
        return self.__links

    def clear(self):
        self.__texts = []
        self.__links = []
        self.__results = []
        self.__totalcount = 0
