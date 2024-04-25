import os

from flask_login import login_user, LoginManager, login_required, logout_user, current_user
import requests

from data import db_session
from data.users import User
from forms.user import LoginForm, RegisterForm
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/krypto.db")

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect("/lobby")
    return redirect("/login")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="There is already such a user")
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Password mismatch")

        user = User(
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html', title="Authorization",
                               message="Incorrect login or password",
                               form=form)
    return render_template('login.html', title="Authorization", form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/register")


@app.route('/lobby', methods=['GET', 'POST'])
@login_required
def lobby():
    data = get_coins()
    return render_template('main_page.html', data=data)


def get_coins():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    api_key = "54d0320a-dc81-47c8-8f1c-217a128162f7"
    start = 1
    limit = 30
    convert = 'USD'
    percent_change = 'percent_change_24h'

    headers = {
        "X-CMC_PRO_API_KEY": api_key,
        'Accepts': 'application/json'
    }
    params = {
        'start': start,
        'limit': limit,
        'convert': convert
    }
    try:
        response = requests.get(url, headers=headers, params=params).json()['data']
    except Exception as e:
        print(e)
        return redirect("/logout")

    data = [{
        "symbol": f"{item["symbol"]}",
        "name": f"{item["name"]}",
        "price": float(f"{round(item["quote"][convert]["price"], 2)}"),
        "percent_change": float(f"{round(item["quote"][convert][percent_change], 4)}")
    } for item in response]

    return data


if __name__ == '__main__':
    main()
