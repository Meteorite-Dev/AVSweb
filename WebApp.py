import os
from flask import send_from_directory
import auth
from flask import Flask
from flask import render_template
from flask_jsglue import JSGlue

from auth.auth import auth
from Webcv.Webcv import webcv
import threading

app = Flask(__name__, template_folder="templates/",static_folder="static/")

jsglue = JSGlue(app)

app.config.from_pyfile('config.py')

app.secret_key = app.config['SECRET_KEY']

app.register_blueprint(auth)
app.register_blueprint(webcv)


@app.route("/")
def home():
    return render_template('welcome.html')


@app.route("/test")
def test():
    return render_template('test.html')


@app.route('/static/images/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='images/icon.ico')


if __name__ == "__main__":

    app.run()
