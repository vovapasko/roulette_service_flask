import os
import traceback
from datetime import datetime

from flask import request, url_for, render_template, Flask, session
from werkzeug.utils import redirect

from root.db import Database
from root.entities import Bet, Player
from root.tools import correct_bet, generate_bet, format_player_bet, \
    calculate_bet_result, generate_list, login_required, get_bet_id, generateBetForDb, generateCasinoData, correct_login
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "Secret key"
app.config['SECRET_KEY'] = SECRET_KEY

db = Database()
app.config['SQLALCHEMY_DATABASE_URI'] = db.cstr


# Route for handling the login page logic
def get_users_log_pass():
    users_data = []
    with db:
        users = db.fetchAllPlayers()
        for user in users:
            user_dict = dict()
            user_dict["player_id"] = user.player_username
            user_dict["password"] = user.passwrd
            users_data.append(user_dict)
    return users_data


@app.route('/')
def welcome():
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return redirect("https://super-app-150.herokuapp.com/")
        users_data = get_users_log_pass()
        if correct_login(users_data, request):
            return redirect('/home')
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    lst = generate_list()
    username = session.get('username')
    with db:
        balance = db.fetchPlayer(username).balance
    player = {'username': username, 'balance': balance}
    if request.method == 'POST':
        player_bet_money = request.form['moneyToBet']
        if correct_bet(player_bet_money, balance):
            bet = generate_bet()
            color = request.form['exampleRadios']
            number = request.form['bet_number']
            player_bet = format_player_bet(player_bet_money, color, number)
            bet_result = calculate_bet_result(player_bet, bet)
            new_bet_obj = generateBetForDb(player_bet, bet_result)
            new_casino_obj = generateCasinoData(username, new_bet_obj.bet_id)
            with db:
                db.createBet(new_bet_obj)
                db.createCasino(new_casino_obj)
            new_balance = balance + bet_result['player_win']
            player = {'username': username, 'balance': new_balance}
            with db:
                db.updatePlayerBalance(username, new_balance)
            return render_template('play.html', lst=lst, player=player, bet=str(bet),
                                   player_bet=str(player_bet), bet_result=str(bet_result))
        else:
            error = 'Wrong number! Bet must be number less than ' + str(balance)
            return render_template('play.html', lst=lst, player=player, error=error)
    return render_template('play.html', lst=lst, player=player)


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        users_data = get_users_log_pass()
        user_new_username = request.form['new_username']
        for user_data in users_data:
            if user_data['player_id'] == user_new_username:
                error = "This username already exists"
                return render_template("register.html", error=error)
        new_password = request.form['new_password']
        new_password1 = request.form['new_password1']
        if new_password != new_password1:
            error = "Passwords must match"
            return render_template("register.html", error=error)
        new_player = Player(player_username=user_new_username, balance=1000, passwrd=new_password)
        with db:
            db.createPlayer(new_player)
        session['username'] = user_new_username
        return redirect('home')
    return render_template("register.html", error=error)


@app.route('/player_stat')
def player_stat():
    return "Here comes the stat"


if __name__ == '__main__':
    app.run(debug=True)
