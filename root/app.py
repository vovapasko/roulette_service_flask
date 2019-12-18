import os

from flask import request, url_for, render_template, Flask, session
from werkzeug.utils import redirect

from db import Database
from tools import correct_bet, generate_bet, format_player_bet, \
	calculate_bet_result, generate_list, login_required

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
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
    return render_template('hello.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(session.get('username'))
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return redirect("https://super-app-150.herokuapp.com/")
        users_data = get_users_log_pass()
        for user_data in users_data:
            user_login = user_data['player_id']
            user_passw = user_data['password']
            if request.form['username'] == user_login \
                    and request.form['password'] == user_passw:
                session['username'] = user_login
                with db:
                    balance = db.fetchPlayer(user_login).balance
                    session['player_balance'] = balance
                return redirect('/home')
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    lst = generate_list()
    username = session.get('username')
    balance = session['player_balance']
    player = {'username': username, 'balance': balance}
    if request.method == 'POST':
        player_bet_money = request.form['moneyToBet']
        if correct_bet(player_bet_money, balance):
            bet = generate_bet()
            color = request.form['exampleRadios']
            number = request.form['bet_number']
            player_bet = format_player_bet(player_bet_money, color, number)
            bet_result = calculate_bet_result(player_bet, bet)
            new_balance = balance + bet_result['player_win']
            player = {'username': username, 'balance': new_balance}
            session['player_balance'] = new_balance
            return render_template('play.html', lst=lst, player=player, bet=str(bet),
                                   player_bet=str(player_bet), bet_result=str(bet_result))
        else:
            error = 'Wrong number! Bet must be number less than ' + str(balance)
            return render_template('play.html', lst=lst, player=player, error=error)
    return render_template('play.html', lst=lst, player=player)


@app.route('/logout')
@login_required
def logout():
    username = session['username']
    new_balance = int(session['player_balance'])
    with db:
        db.updatePlayerBalance(username, new_balance)
    session.pop('username', None)
    session.pop('player_balance', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
