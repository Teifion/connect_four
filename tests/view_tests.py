import transaction
import unittest
from ..lib import (
    rules,
)
from ..config import config

# I'm still trying to work out how to make this test plug into the existing
# framework while still being easy to decouple, the code I'm currently
# using is not able to be separated from my framework yet :s
class ViewsTester(unittest.TestCase):
    def test_views(self):
        if config['viewtest_class'] is None:
            self.skipTest("No viewtest class to use for test")
        
        if config['viewtest_function'] == "":
            self.skipTest("No viewtest function name (though we did find a class)")
        
        tester = config['viewtest_class']()
        test_view = getattr(tester, config['viewtest_function'])
        
        with transaction.manager:
            # Main men
            test_view(
                path = "/games/connect4/menu",
                msg = "There was an error displaying the connect four menu"
            )
            
            # Roll it all back so none of our changes are saved
            transaction.abort()
