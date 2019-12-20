import traceback
from datetime import datetime
from random import randrange, choice
from functools import wraps
from flask import session, redirect, url_for, request
import uuid

from root.entities import Bet, Casino


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
    return 0 < float_bet <= balance


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
    bet_result = {'player_win': player_bet['money'], 'color': bet['color'], 'number': bet['number'], 'bet_win': True}
    if player_bet['number'] == bet['number'] == 0:
        bet_result['player_win'] *= 10
    elif player_bet['number'] == bet['number'] and player_bet['color'] == bet['color']:
        bet_result['player_win'] *= 5
    elif player_bet['color'] == bet['color'] and player_bet['number'] == 'None':
        bet_result['player_win'] *= 2
    else:  # bet is lost
        bet_result['player_win'] = -player_bet[
            'money']  # means that player lost his money and his bet money should be subtracted from his balance
        bet_result['bet_win'] = False
    return bet_result


def login_required(route):
    @wraps(route)
    def _(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return route(*args, **kwargs)

    return _


def get_bet_id():
    return str(uuid.uuid4())


def handleBetNumber(bet):
    try:
        int_bet = int(bet['number'])
    except ValueError:
        return None  # means that player didn't bet on number
    return int_bet


def generateBetForDb(player_bet, bet_result):
    try:
        bet_id = get_bet_id()
        bet_money = float(player_bet['money'])
        won_money = float(bet_result['player_win'])
        won_bet = bet_result['bet_win']
        bet_time = get_current_time()
        bet_color = player_bet['color']
        bet_number = handleBetNumber(player_bet)
        return Bet(bet_id=bet_id, bet_money=bet_money, won_money=won_money, won_bet=won_bet,
                   bet_time=bet_time, bet_color=bet_color, bet_number=bet_number)
    except Exception:
        traceback.print_exc()
        return None


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %X")


def generateCasinoData(username, bet_id):
    return Casino(player_username=username, bet_id=bet_id)


def correct_login(users_data, request):
    for user_data in users_data:
        user_login = user_data['player_id']
        user_passw = user_data['password']
        if request.form['username'] == user_login \
                and request.form['password'] == user_passw:
            session['username'] = user_login
            return True
    return False


def validate_money(money):
    try:
        float_money = float(money)
    except ValueError:
        return False
    return float_money > 0
