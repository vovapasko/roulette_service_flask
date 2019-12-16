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
    return {'money': money, 'color': color, 'number': number}


def generate_bet():
    colors = ['black', 'red']
    color = random.choice(colors)
    number = randrange(37)
    return {'color': color, 'number': number}


def calculate_bet_result(player_bet, bet):
    bet_result = {'player_win': player_bet['money'], 'color': bet['color'], 'number': bet['number']}
    if player_bet['number'] == bet['number'] == 0:
        bet_result['player_win'] *= 10
    elif player_bet['number'] == bet['number'] and player_bet['color'] == bet['color']:
        bet_result['player_win'] *= 5
    elif player_bet['color'] == bet['color'] and player_bet['number'] == 'None':
        bet_result *= 2
    else:
        bet_result['player_win'] = 0
    return bet_result
