from flask import render_template, Blueprint, request
from app.forms import *
from app.models import *

blueprint = Blueprint('pages', __name__)


################
# ## routes ####
################


@blueprint.route('/')
def home():
    return render_template('pages/placeholder.home.html')


# TODO: remove
@blueprint.route('/testdb')
def testdb():
    if db.session.query(Dog).first():
        return "it works!"
    else:
        return "it doesn't work :(\n(or there are no Dog objects in the db)"


@blueprint.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@blueprint.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@blueprint.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
