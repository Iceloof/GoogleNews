
### MODULES

from GoogleNews import GoogleNews

### METHODS

def show_routine(results):
    for num,page in enumerate(results):
        print(f"{num}. {page['date']} - {page['title']}")
        
### MAIN

# Setup the research
keywords="covid cava de' tirreni"
period='10d'
google_news = GoogleNews(lang='it',period=period)
google=GoogleNews(lang='it',period=period)

# Results from news.google.com
google_news.get_news(keywords)
results_gnews=google_news.results(sort=True)
show_routine(results_gnews)

# Results from google.com
google.search(keywords)
results_google=google.results(sort=True)
show_routine(results_google)