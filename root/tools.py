import random
from random import randrange


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


def format_player_bet(money, color, number):
    return "player bet"


def generate_bet():
    colors = ['black', 'red']
    color = random.choice(colors)
    number = randrange(37)
    if number == 0:
        return {'number': str(0)}
    return {'color': color, 'number': number}
