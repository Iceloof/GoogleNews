
### MODULES

from GoogleNews import GoogleNews

### METHODS

def show_routine(results):
    for num,page in enumerate(results):
        print(f"{num}. {page['date']} - {page['title']}")
        
### MAIN

# Setup the research
keywords="covid italia"
period='10d'
google_news = GoogleNews(lang='it',period=period)
google=GoogleNews(lang='it',period=period)

# Results from news.google.com
google_news.get_news(keywords)
results_gnews=google_news.result(sort=True)
show_routine(results_gnews)

# Results from google.com
# google_news.clear()
google.search(keywords)
results_google=google.result(sort=True)
show_routine(results_google)