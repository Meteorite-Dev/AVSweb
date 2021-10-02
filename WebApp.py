import auth
from flask import Flask, Blueprint
from flask import render_template
from auth.auth import auth
from Webcv.Webcv import webcv, motion, vs

import threading

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.secret_key = app.config['SECRET_KEY']

app.register_blueprint(auth)
app.register_blueprint(webcv)


@app.route("/")
def hello_world():
    return render_template('welcome.html')


if __name__ == "__main__":
    t = threading.Thread(target=motion)
    t.daemon = True
    t. start()
    app.run()

vs.stop()
