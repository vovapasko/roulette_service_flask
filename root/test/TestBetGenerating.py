import unittest


class TestBetGenerating(unittest.TestCase):
    def test_win_with_number_bet(self):
        player_bet = {'money': 20, 'color': 'black', 'number': 0}
        res_bet = {'color': 'red', 'number': 0, 'bet_win': True}



    def test_win_bet_without_number(self):
        pass