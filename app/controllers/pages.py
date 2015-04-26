from flask import (render_template, Blueprint, request, session, redirect,
                   url_for)
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


# TODO: remove
@blueprint.route('/testdb')
def testdb():
    if db.session.query(Dog).first():
        return "it works!"
    else:
        return "it doesn't work :(\n(or there are no Dog objects in the db)"


@blueprint.route('/about')
@login_required
def about():
    return render_template('pages/placeholder.about.html')


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
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)

            redirect_page = request.args.get("next", "home")
            return redirect(url_for("pages.{0}".format(redirect_page)))

    elif request.method == 'GET':
        return render_template('forms/login.html', form=form)


@blueprint.route('/logout')
def logout():
    # TODO: [why] is this needed?
    # current_user_id = current_user.get_id()
    # if not current_user_id:
    #     # already logged out
    #     return redirect(url_for("pages.home"))
    # user = User.query.get(current_user_id)
    # user.authenticated = False
    # db.session.add(user)
    # db.session.commit()
    logout_user()
    return redirect(url_for("pages.home"))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('forms/register.html', form=form)
        else:
            new_user = form.create_user()
            new_user.authenticated = True
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            return ("registered and logged in?")
    elif request.method == "GET":
        return render_template('forms/register.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
