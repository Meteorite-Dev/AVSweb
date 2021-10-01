from operator import mod
from flask import request, render_template, url_for, redirect, flash
from flask import Blueprint
from flask import render_template
from flask.templating import render_template_string

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from . import models


auth = Blueprint('auth', __name__, template_folder='../templates/auth')

login_manager = LoginManager()


@auth.record_once
def on_load(state):
    login_manager.init_app(state.app)
    models.__init__(state.app)
    with state.app.app_context():
        models.db.create_all()


login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Accessed diened!!'


class User(UserMixin, models.User):
    pass


@login_manager.user_loader
def user_loader(user):
    user = User()
    user.id = request.form.get('user_id')
    return user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    user = User()
    lus = request.form['user_id']
    cus = models.User().query.filter_by(name=lus).first()
    if cus != None:
        if request.form['password'] == cus.password:
            print("login")
            login_user(user)
            return redirect(url_for('auth.dash'))
        else:
            print("pas error")
            flash("Access denied!!")
            return redirect(url_for('auth.login'))
    else:
        print("user error")
        flash("Can not find user.")
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'


@auth.route('/dashboard')
@login_required
def dash():
    return render_template('dashboard.html')


# @login_manager.request_loader
# def request_loader(request):
#     使用者 = request.form.get('user_id')
#     if 使用者 not in users:
#         return

#     user = User()
#     user.id = 使用者

#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['password'] == users[使用者]['password']

#     return user


# @ auth.route("/show_records")
# @ login_required
# def show_records():
#     python_records = web_select_overall()
#     return render_template("show_records.html", html_records=python_records)
