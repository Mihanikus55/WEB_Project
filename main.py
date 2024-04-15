import os

from forms.user import LoginForm
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# @app.route("/", methods=['GET', 'POST']) # временно
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
    return render_template('login.html', form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
