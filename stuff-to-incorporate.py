


def getpage():
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