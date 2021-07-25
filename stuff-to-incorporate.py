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


            response = requests.get(self.url_, headers=self.headers, cookies=cookies)