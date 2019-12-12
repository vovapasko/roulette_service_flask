import os

from flask import request, url_for, render_template, Flask
from werkzeug.utils import redirect

from root.db import Database

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db = Database()
app.config[
    'SQLALCHEMY_DATABASE_URI'] = db.cstr


# Route for handling the login page logic
def get_users_log_pass():
    users = db.fetchAllPlayers()
    users_data = []
    for user in users:
        user_dict = {}
        user_dict["player_id"] = str(user.player_id)
        user_dict["password"] = user.passwrd
        users_data.append(user_dict)
    return users_data


@app.route('/')
def welcome():
    return render_template('hello.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' or request.form['password'] == 'admin':
            return redirect("https://super-app-150.herokuapp.com/")
        users_data = get_users_log_pass()
        for user_data in users_data:
            user_login = user_data['player_id']
            user_passw = user_data['password']
            if request.form['username'] == user_login \
                    and request.form['password'] == user_passw:
                str = request.form['username'] + " + " + request.form['password']
                return str
        error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/home')
def home():
    return "home"


if __name__ == '__main__':
    app.run(debug=True)
