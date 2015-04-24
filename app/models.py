from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '<Dog {0}>'.format(self.name)
