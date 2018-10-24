from bs4 import BeautifulSoup
import urllib.request as req
from core.util import strings

class Tweet:

    def __init__(self, soup):
    
        self.soup = soup
        self.soup_text = soup.find(name='p', attrs={'class': 'tweet-text'})
        self.text = self.soup_text.text
        self.cleantext = strings.stripurl.sub(string=self.text, repl="")

        
    def getTweets(page):
        page=req.urlopen(url=page)
        soup=BeautifulSoup(page, 'html.parser')
        outertwts=soup.findAll(name='div', attrs={'class':'tweet',
                                                  'data-screen-name':'jon_bois'})
        
        tweets=[Tweet(s) for s in outertwts]
        return tweets