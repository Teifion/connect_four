import unittest
from dashboard.games.connect_four.lib import (
    rules,
    actions,
)

# Remember the board is stored upside down
current_state = """
12-1212
12-2121
--11212
12-----
12-2222
12-1111
""".replace("\n", "").replace(" ", "").replace("-", " ")

class RulesTester(unittest.TestCase):
    def test_get_place_position(self):
        vals = (
            ((0, 0), 0),
            ((1, 0), 7),
            ((5, 5), 40),
            ((5, 6), 41),
        )
        
        for (row, col), expected in vals:
            self.assertEqual(rules.get_place_position(row, col), expected)
    
    def test_first_empty(self):
        vals = (
            ("01234 6", 5),
            (" 123456", 0),
            ("0   456", 1),
        )
        
        for column_sequence, expected in vals:
            self.assertEqual(rules.first_empty(column_sequence), expected)
    
    def test_column(self):
        expected_results = (
            "11 111",
            "22 222",
            "  1   ",
            "121 21",
            "212 21",
            "121 21",
            "212 21",
        )
        
        for col, expected in enumerate(expected_results):
            result = list(rules.column(current_state, col))
            expected = list(expected)
            self.assertEqual(result, expected)
    
    def test_check_for_game_end(self):
        empty_state = " " * (7*6)
        
        horrizontal_win = """
        ---1-2-
        ---2-1-
        1111-1-
        ---1-2-
        ---2-1-
        ---1-2-
        """.replace("\n", "").replace(" ", "").replace("-", " ")
        
        vertical_win = """
        ---2---
        ---22--
        11-12--
        ---22--
        ---22--
        ---2111
        """.replace("\n", "").replace(" ", "").replace("-", " ")
        
        # Remember the board is drawn upside down
        tl_br_win = """
        -------
        -----1-
        ----1--
        ---1---
        --1----
        -------
        """.replace("\n", "").replace(" ", "").replace("-", " ")
        
        bl_tr_win = """
        -------
        --1----
        ---1---
        ----1--
        -----1-
        -------
        """.replace("\n", "").replace(" ", "").replace("-", " ")
        
        # These are ones that should have had a win when I played but didn't
        other_tl_br_win = " 1112   212    12     2                   "
        self.assertEqual(True, rules._check_upleft_lowright_diagonal(other_tl_br_win))
        
        # Check we win only on the ones we want to win
        self.assertEqual(None, rules._check_horrizontal_end(empty_state))
        self.assertEqual(True, rules._check_horrizontal_end(horrizontal_win))
        self.assertEqual(None, rules._check_horrizontal_end(vertical_win))
        self.assertEqual(None, rules._check_horrizontal_end(bl_tr_win))
        self.assertEqual(None, rules._check_horrizontal_end(tl_br_win))
        
        self.assertEqual(None, rules._check_vertical_end(empty_state))
        self.assertEqual(None, rules._check_vertical_end(horrizontal_win))
        self.assertEqual(True, rules._check_vertical_end(vertical_win))
        self.assertEqual(None, rules._check_vertical_end(bl_tr_win))
        self.assertEqual(None, rules._check_vertical_end(tl_br_win))
        
        self.assertEqual(None, rules._check_lowleft_upright_diagonal(empty_state))
        self.assertEqual(None, rules._check_lowleft_upright_diagonal(horrizontal_win))
        self.assertEqual(None, rules._check_lowleft_upright_diagonal(vertical_win))
        self.assertEqual(True, rules._check_lowleft_upright_diagonal(bl_tr_win))
        self.assertEqual(None, rules._check_lowleft_upright_diagonal(tl_br_win))
        
        self.assertEqual(None, rules._check_upleft_lowright_diagonal(empty_state))
        self.assertEqual(None, rules._check_upleft_lowright_diagonal(horrizontal_win))
        self.assertEqual(None, rules._check_upleft_lowright_diagonal(vertical_win))
        self.assertEqual(None, rules._check_upleft_lowright_diagonal(bl_tr_win))
        self.assertEqual(True, rules._check_upleft_lowright_diagonal(tl_br_win))
        
        # Check overall function
        self.assertEqual(False, rules.check_for_game_end(empty_state))
        self.assertEqual(True, rules.check_for_game_end(current_state))
        self.assertEqual(True, rules.check_for_game_end(horrizontal_win))
        self.assertEqual(True, rules.check_for_game_end(vertical_win))
        self.assertEqual(True, rules.check_for_game_end(bl_tr_win))
        self.assertEqual(True, rules.check_for_game_end(tl_br_win))
