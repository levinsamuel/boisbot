
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from core.types import Tweet
from core.util import mylog

log = mylog.get_logger("seleniumutils")


class TweetFinder:

    """Class for handling Selenium-based tweet searches"""

    def __init__(self):
        self.browser = webdriver.Chrome()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.browser.quit()

    def get_body(self):
        return self.browser.find_element_by_tag_name('body')

    def search_tweets(self, user, date_before=None):
        """Direct the browser to the tweets by the given user from before the
    given date."""

    #https://twitter.com/search?f=tweets&q=from%3Ajon_bois%20-filter%3Aretweets%20-filter%3Areplies&src=typd

        # Date in yyyy-mm-dd format
        url = (f"https://twitter.com/search?f=tweets&q=from%3A{user}"
               "%20-filter%3Aretweets%20-filter%3Areplies")
        if date_before is not None:
            url += f"%20until%3A{date_before.isoformat()}"

        log.debug("Querying URL: %s", url)
        self.browser.get(url)
        self.twlist = WebDriverWait(
                self.browser, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, 'stream-items-id')
                    )
                )

    def count_visible_tweets(self):

        try:
            return len(self.twlist.find_elements_by_class_name('stream-item'))
        except AttributeError:
            log.error("Browser has no visible tweets.")
            raise

    def find_tweets_in_view(self, user):
        """Get the tweet objects from all tweets currently in the view.

    Returns: an array of core.types.Tweet objects."""

        tweets = [Tweet(html) for html in self.browser.find_elements_by_xpath(
            "//div[contains(@class, 'tweet')][@data-screen-name='{}']".
            format(user))]

        return tweets

    def user_found(self):

        try:
            self.browser.find_element_by_xpath(
                "//div[@class='errorpage-body-content']/h1")
            return False;
        # Error message not found, user is found
        except NoSuchElementException:
            return True;
