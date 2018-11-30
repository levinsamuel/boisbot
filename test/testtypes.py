from core.types import WeightsFile
import unittest
from core.util import mylog
import datetime as dt

log = mylog.get_logger('testtypes')
log.setLevel(mylog.logging.DEBUG)


class TestTypes(unittest.TestCase):

    def test_create_filename(self):

        fn = WeightsFile._get_checkpoint_file(None, 'jb', 20, 1.2, 3)
        log.debug("Filename: %s", fn)

        wf = WeightsFile(None, None, "jb")
        log.debug("filename: %s", wf.create_filename())

    def test_dates(self):

        mytime = 1542395192
        mydt = dt.date.fromtimestamp(mytime)
        log.debug("formatted date: %s", mydt.isoformat())
        self.assertEqual('2018-11-16', mydt.isoformat())
