# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 17:04:46 2020

@author: mario
"""

import urllib.request
from bs4 import BeautifulSoup as Soup
from dateutil.parser import parse

lang='it'
period='7d'
key="cava de' tirreni"
key = "+".join(key.split(" "))
url = 'https://news.google.com/search?q={}+when:{}&hl={}'.format(key,period,lang.lower())
try:
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    page = response.read()
    content = Soup(page, "html.parser")
    articles = content.select('div[class="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"]')
    
    results=[]
    for article in articles:
        try:
            # title
            try:
                title=article.find('h3').text
            except:
                title=None
            # description
            try:
                description=article.find('span').text
            except:
                description=None
            # date
            try:
                date = article.find("time").text
            except:
                date = None
            # datetime
            try:
                datetime_chars=article.find('time').get('datetime')
                datetime_obj = parse(datetime_chars).replace(tzinfo=None)
            except:
                datetime_obj=None
            # link
            try:
                link='news.google.com/' + article.find("h3").find("a").get("href")
            except:
                link = None
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
            results.append({'title':title,
                            'description':description,
                            'date':date,
                            'datetime':datetime_obj,
                            'link':link,
                            'img':img,
                            'site':site,
                            })
        except Exception as e_article:
            print(e_article)
except Exception as e_parser:
    print(e_parser)
    pass


        
            