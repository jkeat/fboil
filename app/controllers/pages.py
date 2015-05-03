from flask import (render_template, Blueprint, request, session,
                   redirect, url_for, flash, abort)
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from itsdangerous import URLSafeSerializer, BadSignature
from app.forms import *
from app.models import *
from app.decorators import activated_required
from app.email import send_email

pages_blueprint = Blueprint('pages', __name__)


@pages_blueprint.route('/')
def home():
    return render_template('pages/home.html')


@pages_blueprint.route('/about')
def about():
    return render_template('pages/about.html')


@pages_blueprint.route('/secret')
@login_required
@activated_required
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


def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = "buttfacepoop123"  # TODO: app.secret_key
    return URLSafeSerializer(secret_key)


def get_activation_link(user):
    s = get_serializer()
    token = s.dumps(user.id)
    return url_for('pages.activate_user', token=token, _external=True)


def email_user_activation_link(user):
    subject = "Please confirm your email address"
    activation_link = get_activation_link(user)
    html = render_template('pages/emails/activate.html',
                           activation_link=activation_link)
    send_email(user.email, subject, html)


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

            email_user_activation_link(new_user)

            flash("Account created successfully! Please confirm your email.")
            return redirect(url_for("pages.home"))
    elif request.method == "GET":
        return render_template('pages/forms/register.html', form=form)


@pages_blueprint.route('/users/activate/<token>')
def activate_user(token):
    s = get_serializer()
    try:
        user_id = s.loads(token)
    except BadSignature:
        abort(404)

    user = User.query.get_or_404(user_id)
    user.activate()
    flash("Your account has been activated!")
    return redirect(url_for("pages.home"))
