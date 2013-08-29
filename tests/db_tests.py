import transaction
import unittest
from ..lib import (
    rules,
)
from ..config import config

"""
I've got a class defined in test_f which does the following.

class DBTestClass(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = routes(testing.setUp())
    
    def tearDown(self):
        DBSession.execute("ROLLBACK")
        self.session.remove()

Sadly I couldn't work out how to detatch this part from my
main framework. The key part is it'll allow us to use the db connection.
"""

try:
    from ....core.lib.test_f import DBTestClass
except Exception:
    class DBTestClass(object):
        pass

class DBTester(DBTestClass):
    def test_game(self):
        pass
        
        # get_profile(user_id)
        # add_empty_profile(user_id)
        # get_game_list(user_id)
        # get_waiting_game_list(user_id)
        # get_recent_game_list(user_id, limit=5)
        # find_user(identifier)
        # new_game(p1, p2, rematch=None)
        # get_game(game_id)
        # add_turn(the_game, column)
        # end_game(the_game)
        # draw_game(the_game)
        # perform_move(the_game, column)
        # completed_games(user_id, opponent_id=None)
        # games_in_progress(user_id, opponent_id=None)
        # games_won(user_id, opponent_id=None)
        # games_lost(user_id, opponent_id=None)
        # games_drawn(user_id, opponent_id=None)
        # get_stats(user_id, opponent_id=None)
