from unittest import TestCase
from core.util import web, mylog
from core.errors import NotFound
import logging

log = mylog.get_logger('webtest')
log.setLevel(logging.DEBUG)


class TestWebUtils(TestCase):

    def test_get_icon(self):

        log.debug('user found url: %s', web.get_icon('deepestcat'))
        try:
            web.get_icon('thedeeperercatt')
            self.fail("Should throw not found")
        except NotFound:
            log.debug("not found error raised as expected")
