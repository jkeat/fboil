from flask import (render_template, Blueprint)
from flask.ext.login import login_required
from app.decorators import confirmed_email_required


pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
    return render_template('pages/home.html')


@pages.route('/about')
def about():
    return render_template('pages/about.html')


@pages.route('/secret')
@login_required
@confirmed_email_required
def secret():
    return render_template('pages/secret.html')
