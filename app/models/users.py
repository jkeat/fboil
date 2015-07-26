from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import or_, func
from ..extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    email = db.Column(db.String(255), unique=True)
    confirmed_email = db.Column(db.Boolean(), default=False)

    passhash = db.Column(db.String(255))

    is_oauth_user = db.Column(db.Boolean(), default=False)
    twitter_username = db.Column(db.String(255), unique=True)

    def __init__(self, password=None, **kwargs):
        super(User, self).__init__(**kwargs)
        if password:
            self.set_password(password)

    def __repr__(self):
        return '<User {0} ({1})>'.format(self.username, self.id)

    def set_password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

    def confirm_email(self):
        self.confirmed_email = True
        db.session.add(self)
        db.session.commit()

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
