from flask import (render_template, Blueprint, request, session,
                   redirect, url_for, flash)
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from app.forms import *
from app.models import *

pages_blueprint = Blueprint('pages', __name__)


################
# ## routes ####
################


@pages_blueprint.route('/')
def home():
    return render_template('pages/home.html')


@pages_blueprint.route('/about')
def about():
    return render_template('pages/about.html')


@pages_blueprint.route('/secret')
@login_required
def secret():
    return render_template('pages/secret.html')


@pages_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for("pages.home"))

    form = LoginForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            return render_template('pages/forms/login.html', form=form)
        else:
            user = form.get_user()
            login_user(user, remember=True)
            redirect_page = request.args.get("next", url_for("pages.home"))
            return redirect(redirect_page)

    elif request.method == 'GET':
        return render_template('pages/forms/login.html', form=form)


@pages_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("pages.home"))


@pages_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for("pages.home"))

    form = RegisterForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('pages/forms/register.html', form=form)
        else:
            new_user = form.create_user()
            login_user(new_user, remember=True)

            flash("Account created successfully!")
            return redirect(url_for("pages.home"))
    elif request.method == "GET":
        return render_template('pages/forms/register.html', form=form)
