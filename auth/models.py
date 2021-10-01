from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def __init__(app):
    db.init_app(app)


class User(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))



