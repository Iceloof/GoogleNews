import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import locale
import random
from datetime import date
from datetime import timedelta
import time
from automatic_scrape.automatic_funcs import find_date
import requests
from sentry_sdk import capture_exception

from contextlib import contextmanager

# import browser_cookie3

import logging
logger = logging.getLogger(__name__)
import pickle

class ScrapeGoogle():


    def google_news_scrape(self, **kwargs):
        do_continue = True
        googlenews = GoogleNewsBaken()
        locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')
        page = 1
        zoekterm = kwargs['zoekterm']
        branche = kwargs['branche']
        subbranche = kwargs['subbranche']
        googlenews.search(str(zoekterm))
        while do_continue:

            time.sleep(random.randint(1, 3))
            resultaat = googlenews.result()
            #loop over the results in "resultaat"
            for i in range(len(resultaat)):
                nieuws_bron = delete_pers_blog(resultaat[i]['media']).strip() #hier gaat de nieuwsbron door een script dat persbericht en blog verwijderd
                article = {"attributes": {"scrape_source": "Google_"+str(branche), "news_source": str(nieuws_bron),
                                          "dt_posted": find_date(resultaat[i]['date']),
                                          "title": resultaat[i]['title'], "body": resultaat[i]['desc'],
                                          "url": resultaat[i]['link'], 'tag': zoekterm,
                                          'input': resultaat[i]['title'] +' ' + resultaat[i]['desc'],
                                          'branche': str(branche),
                                          'labels': {"Branche": [subbranche], "Onderwerp": "", "Doelgroep": ""}},
                           "type": "sample"}
                if article["attributes"]['title']== None or article["attributes"]['body'] == None or \
                        article["attributes"]['url'] == None: raise ValueError(f'url, title or description not found."')
                yield article
            page += 1
            googlenews.clear()
            do_continue = googlenews.getpage(page) #returns false if anything is wrong hence scrape will not continue




class GoogleNewsBaken():

    def __init__(self):
        self.texts = []
        self.links = []
        self.results = []

    def search(self, key):
        self.key = "+".join(key.split(" "))
        self.getpage()

    def getpage(self, page=1):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0']
        self.user_agent = random.choice(user_agents)
        # self.headers = {'User-Agent': self.user_agent}
        self.headers = {'User-Agent': self.user_agent, "Accept-Language": 'nl-NL,nl;q=0.9',"accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        self.url = "https://www.google.nl/search?q=" + self.key + "&tbm=nws&start=" + str(
            (10 * (page - 1))) + "&tbs=sbd:1"
        try:

            with GetRequests(self.url, self.headers).open_url() as google_results:
                result = google_results.find_all("div", class_="dbsr")
                if len(result) == 0:
                    # if there are empty pages, process of google news must stop
                    logger.info(f"empty results found at '{self.url}")
                    return False

                for item in result:
                    self.results.append(
                        {'title': item.find(role='heading').text, 'media': item.find(class_="XTjFC WF4CUc").text,
                         'date': item.find(class_="yJHHTd").find_all("span")[0].text,
                         'desc': item.find(class_='Y3v8qd').text,
                         'link': item.find("a").get("href")})
                return True

        except Exception as e:
            # if anything happened which is not correct, script returns False and logs the error
            logger.info(f"stopped working and found an error at '{self.url}")
            logger.error(e)
            capture_exception(e)
            return False


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


def find_date_gn(data):
    try:
        a = datetime.strptime(data, "%d %b. %Y").date()
    except:
        try:
            a = datetime.strptime(data, "%d %b %Y").date()
        except:
            try:
                value, unit, _ = data['date'].split()  # dit doen als er ... minuten/uur/seconden geleden staat
                if unit == 'uur':
                    uur = datetime.now().hour
                    if int(value) <= uur:
                        a = date.today()
                    else:
                        a = date.today() - timedelta(days=1)
                if unit != 'uur':
                    a = date.today()
            except:
                a = date.today()

    a = a.isoformat()  # terug schrijven naar ISO format
    if len(a) < 11: a += " 00:00:00"
    return a


def delete_pers_blog(string):
    out = string.replace("(persbericht)","")
    out = out.replace("(Blog)", "")
    return out

class GetRequests():
    def __init__(self, url, headers):
        self.headers = headers
        self.url_ = url

    @contextmanager
    def open_url(self):
        try:
            # get the content and use beautifulsoup
            # open the saved cookie jar
            with open('google_news_cookiejar', 'rb') as f:
                cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            logger.info(f" the cookies for google.nl: '{cookies}'")
            # add cookies to the request
            response = requests.get(self.url_, headers=self.headers, cookies=cookies)
            logger.info(f" the info/headers from google request opened: '{response.headers}'")
            items = BeautifulSoup(response.content, features='html.parser')
            yield items
        except Exception as e:
            logger.info(e)
        finally:
            # close connection
            response.close()
            items = None
