from werkzeug import generate_password_hash, check_password_hash
from .extensions import db


class Dog(db.Model):
    __tablename__ = 'dogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '<Dog {0}>'.format(self.name)


class User(db.Model):
    # TODO: login method

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(255), unique=True)
    passhash = db.Column(db.String(255))

    def __init__(self, username, email, password):
        self.username = username.lower()
        self.email = email.lower()
        self.set_password(password)

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def set_password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

    # Flask-Login required methods vvv
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    # end Flask-Login required methods ^^^
