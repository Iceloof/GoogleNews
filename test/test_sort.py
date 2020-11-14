# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:13:35 2020

@author: mario
"""

import GoogleNews.__init__ as GoogleNews

googlenews = GoogleNews.GoogleNews()
googlenews.setlang('it')
googlenews.setperiod('1d')
# googlenews.setTimeRange('11/02/2020','11/05/2020')
googlenews.setencode('utf-8')
key="cava de' tirreni"
# timespan_news=googlenews.search(key)
last_news=googlenews.get_news2(key)
last_news[0]
aa=last_news[0].find('time')
aa.attrs['datetime'].replace(tzinfo=None)

# for num,page in enumerate(timespan_news):
#     print(f"{num}. {page['date']}") # see item n. 7
    
# for num,page in enumerate(last_news):
#     print(f"{num}. {page['date']}") # see item n. 7