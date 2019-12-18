from random import randrange, choice
from functools import wraps
from flask import session, redirect, url_for, request


def generate_list():
    lst = []
    lst.append("None")
    for i in range(37):
        lst.append(str(i))
    return lst


def correct_bet(player_bet, balance):
    try:
        float_bet = float(player_bet)
    except ValueError:
        return False
    return float_bet <= balance


def format_player_bet(money, color, number):
    try:
        int_number = int(number)
    except ValueError:
        return {'money': float(money), 'color': color, 'number': number}
    return {'money': float(money), 'color': color, 'number': int_number}


def generate_bet():
    colors = ['black', 'red']
    color = choice(colors)
    number = randrange(37)
    return {'color': color, 'number': number}


def calculate_bet_result(player_bet, bet):
    bet_result = {'player_win': player_bet['money'], 'color': bet['color'], 'number': bet['number']}
    if player_bet['number'] == bet['number'] == 0:
        bet_result['player_win'] *= 10
    elif player_bet['number'] == bet['number'] and player_bet['color'] == bet['color']:
        bet_result['player_win'] *= 5
    elif player_bet['color'] == bet['color'] and player_bet['number'] == 'None':
        bet_result['player_win'] *= 2
    else:
        bet_result['player_win'] = -player_bet[
            'money']  # means that player lost his money and his bet money should be subtracted from his balance
    return bet_result


def login_required(route):
    @wraps(route)
    def _(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return route(*args, **kwargs)

    return _
