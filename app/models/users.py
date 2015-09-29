from sqlalchemy import or_, func
from ..extensions import db
from flask.ext.security import UserMixin, RoleMixin


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role {0}>'.format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    email = db.Column(db.String(255), unique=True)

    password = db.Column(db.String(255))

    is_oauth_user = db.Column(db.Boolean(), default=False)
    twitter_username = db.Column(db.String(255), unique=True)

    # flask-security
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {0} ({1})>'.format(self.username, self.id)

    # ========= Flask-Login required methods vvv
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    # ========= end Flask-Login required methods ^^^

    @classmethod
    def get_by_email_or_username(cls, identification):
        identification = identification.lower()
        return cls.query.filter(or_(func.lower(cls.username) == identification,
                                    func.lower(cls.email) == identification)).first()

    @classmethod
    def is_username_taken(cls, username):
        username = username.lower()
        return (cls.query.filter(func.lower(cls.username) == username).first() is not None)

    @classmethod
    def is_email_taken(cls, email):
        email = email.lower()
        return (cls.query.filter(func.lower(cls.email) == email).first() is not None)

    @classmethod
    def make_unique_username(cls, starter):
        if not cls.is_username_taken(starter):
            return starter
        else:
            number_addon = 1
            while True:
                new_username = "{0}{1}".format(starter, number_addon)
                if not cls.is_username_taken(new_username):
                    return new_username
                number_addon += 1
