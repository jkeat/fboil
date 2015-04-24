from flask.ext.sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)
db.create_all()


class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '<Dog {0}>'.format(self.name)
