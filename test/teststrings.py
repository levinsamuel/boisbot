import unittest
from core.util import strings

class StringsTest(unittest.TestCase):
    
    def test_clean(self):
        
        mytweet="we wrote a bunch of scary short stories at @sbnation. i wrote one about a pitcher with a 0.11 era"
        result=strings.clean(mytweet)
        print(result)
        
        mytweet2="""my favorite hitters to watch ever:

1. griffey (cleanest swing)
2. altuve (best-engineered swing)
3. vlad (batted like he was playing pong)
4. willie mcgee (swung like he wished baseball was never invented)
5. francoeur (likely had never heard of baseball)"""
        result=strings.clean(mytweet2)
        print(result)