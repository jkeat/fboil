from flask import (render_template, Blueprint)
from flask.ext.login import login_required
from ..decorators import confirmed_email_required


pages_blueprint = Blueprint('pages', __name__)


@pages_blueprint.route('/')
def home():
    return render_template('pages/home.html')


@pages_blueprint.route('/about')
def about():
    return render_template('pages/about.html')


@pages_blueprint.route('/secret')
@login_required
@confirmed_email_required
def secret():
    return render_template('pages/secret.html')
