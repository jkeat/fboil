from flask import (render_template, Blueprint, request, session, redirect,
                   url_for, flash)
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from app.forms import *
from app.models import *

blueprint = Blueprint('pages', __name__)


################
# ## routes ####
################


@blueprint.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@blueprint.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@blueprint.route('/secret')
@login_required
def secret():
    return render_template('pages/placeholder.secret.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for("pages.home"))

    form = LoginForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            return render_template('forms/login.html', form=form)
        else:
            user = form.get_user()
            login_user(user, remember=True)
            redirect_page = request.args.get("next", url_for("pages.home"))
            return redirect(redirect_page)

    elif request.method == 'GET':
        return render_template('forms/login.html', form=form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("pages.home"))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for("pages.home"))

    form = RegisterForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('forms/register.html', form=form)
        else:
            new_user = form.create_user()
            login_user(new_user, remember=True)

            return ("registered and logged in?")
    elif request.method == "GET":
        return render_template('forms/register.html', form=form)
