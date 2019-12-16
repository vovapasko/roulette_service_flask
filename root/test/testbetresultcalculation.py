import unittest

from root.tools import calculate_bet_result


class TestBetResultCalculation(unittest.TestCase):
    def test_bet_on_zero(self):
        player_bet = {'money': 20, 'color': 'black', 'number': 0}
        bet = {'color': 'red', 'number': 0}
        result = calculate_bet_result(player_bet, bet)
        expected_win = 200
        actual_win = result['player_win']
        self.assertEqual(actual_win, expected_win)

    def test_bet_on_number_color(self):
        player_bet = {'money': 20, 'color': 'black', 'number': 15}
        bet = {'color': 'black', 'number': 15}
        result = calculate_bet_result(player_bet, bet)
        expected_win = 100
        actual_win = result['player_win']
        self.assertEqual(actual_win, expected_win)

    def test_bet_on_color(self):
        player_bet = {'money': 20, 'color': 'black', 'number': 'None'}
        bet = {'color': 'black', 'number': 23}
        result = calculate_bet_result(player_bet, bet)
        expected_win = 40
        actual_win = result['player_win']
        self.assertEqual(actual_win, expected_win)

    def test_lost_bet_number_color(self):
        player_bet = {'money': 20, 'color': 'black', 'number': 32}
        bet = {'color': 'red', 'number': 23}
        result = calculate_bet_result(player_bet, bet)
        expected_win = -20
        actual_win = result['player_win']
        self.assertEqual(actual_win, expected_win)

    def test(self):
        player_bet = {'money': '12', 'color': 'black', 'number': 'None'}
        bet = {'color': 'black', 'number': 20}
        bet_res = calculate_bet_result(player_bet, bet)

if __name__ == '__main__':
    unittest.main()
