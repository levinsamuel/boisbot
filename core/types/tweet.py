from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement
from core.util import strings
import urllib.request as req

class Tweet:

    def __init__(self, soup):
    
        if type(soup) == 'bs4.BeautifulSoup':
            self.soup_text = soup.find(name='p', attrs={'class': 'tweet-text'})
        elif type(soup) == 'selenium.webdriver.remote.webelement.WebElement':
            self.soup_text = soup.find_element_by_class_name('tweet-text')
        else:
            raise Exception("Unsupported parser type: " + type(soup))
        
        self.soup = soup
        self.text = self.soup_text.text
        self.cleantext = strings.strip_url(self.text)

        
def get_tweets(page):
    page=req.urlopen(url=page)
    soup=BeautifulSoup(page, 'html.parser')
    outertwts=soup.findAll(name='div', attrs={'class':'tweet',
                                              'data-screen-name':'jon_bois'})

    tweets=[Tweet(s) for s in outertwts]
    return tweets