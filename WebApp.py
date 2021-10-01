import auth
from flask import Flask, Blueprint
from flask import render_template
from auth.auth import auth

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.secret_key = app.config['SECRET_KEY']

app.register_blueprint(auth)


@app.route("/")
def hello_world():
    return render_template('welcome.html')


if __name__ == "__main__":
    app.run()
