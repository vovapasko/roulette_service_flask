def generate_list():
    lst = []
    for i in range(37):
        lst.append(str(i))
    lst.append("None")
    return lst


def correct_bet(player_bet, balance):
    try:
        float_bet = float(player_bet)
    except ValueError:
        return False
    return float_bet <= balance
