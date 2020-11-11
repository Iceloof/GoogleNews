# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:13:35 2020

@author: mario
"""

import GoogleNews.__init__ as GoogleNews

googlenews = GoogleNews.GoogleNews()
googlenews.setlang('ita')
googlenews.setTimeRange('11/02/2020','11/05/2020')
googlenews.setencode('utf-8')
googlenews.search('covid firenze')
result=googlenews.result(sort=True)

for num,page in enumerate(result):
    print(f"{num}. {page['date']}") # see item n. 7