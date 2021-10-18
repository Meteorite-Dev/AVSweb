from flask import request, render_template, url_for, redirect, flash
from flask import Blueprint
from flask import render_template

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from . import models


auth = Blueprint('auth', __name__, template_folder='../templates/')

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


class Users(models.User):
    pass


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(usid):
    user = User()
    user.id = usid
    return user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("auth/login.html")
    user = User()
    user.id = request.form.get('user_id')
    usid = request.form.get('user_id')
    cus = Users().query.filter_by(name=user.id).first()
    if cus != None:
        if request.form.get('password') == cus.password:
            print("login")
            print(user.id)
            login_user(user)
            # return render_template("webcv/cv.html")
            # return redirect(url_for('auth.dash'))
            return redirect(url_for('auth.rehome'))
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
    return render_template('welcome.html')


@auth.route('/dashboard')
@login_required
def dash():
    if current_user.is_active:
        return render_template('auth/dashboard.html', user_id=current_user.id)


@auth.route('/callback')
def rehome():
    if current_user.is_active:
        print(current_user.id)
        return render_template('welcome.html', user_id=current_user.id)


@login_manager.request_loader
def request_loader(request):
    user = request.form.get('user_id')
    users = Users().query.with_entities(Users.name)
    if user not in users:
        return
    user = User()
    user.id = request.form.get('user_id')

    cus = users().query.filter_by(name=user.id).first()
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form.get('password') == cus

    return user


# @ auth.route("/show_records")
# @ login_required
# def show_records():
#     python_records = web_select_overall()
#     return render_template("show_records.html", html_records=python_records)
