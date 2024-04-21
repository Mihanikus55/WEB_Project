import os

from data import db_session
from data.users import User
from forms.user import LoginForm, RegisterForm
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/krypto.db")

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.route("/")
def index():
    return ""


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    # if form.validate_on_submit():
    #     if form.password.data != form.password_again.data:
    #         return render_template('register.html', title='Регистрация',
    #                                form=form,
    #                                message="Пароли не совпадают")
    #     db_sess = db_session.create_session()
    #     if db_sess.query(User).filter(User.email == form.email.data).first():
    #         return render_template('register.html', title='Регистрация',
    #                                form=form,
    #                                message="Такой пользователь уже есть")
    #     user = User(
    #         name=form.name.data,
    #         email=form.email.data,
    #         about=form.about.data
    #     )
    #     user.set_password(form.password.data)
    #     db_sess.add(user)
    #     db_sess.commit()
    #     return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     user = db_sess.query(User).filter(User.email == form.email.data).first()
    #     if user and user.check_password(form.password.data):
    #         login_user(user, remember=form.remember_me.data)
    #         return redirect("/")
    #     return render_template('login.html',
    #                            message="Неправильный логин или пароль",
    #                            form=form)
    return render_template('login.html', title="Authorization", form=form)


@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    return render_template('main_page.html', title="MiVa")


if __name__ == '__main__':
    main()
