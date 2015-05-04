from flask import (render_template, Blueprint, request, session,
                   redirect, url_for, flash, abort)
from flask import current_app as APP
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from itsdangerous import URLSafeSerializer, BadSignature
from app.forms import *
from app.models import *
from app.decorators import confirmed_email_required, unconfirmed_email_required
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
@confirmed_email_required
def secret():
    return render_template('pages/secret.html')


@pages_blueprint.route('/confirm-email')
@login_required
@unconfirmed_email_required
def need_confirm_email():
    return render_template('pages/confirm-email.html')


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

            email_user_confirmation_link(new_user)

            flash("Account created successfully! Please confirm your email.")
            return redirect(url_for("pages.home"))
    elif request.method == "GET":
        return render_template('pages/forms/register.html', form=form)


@pages_blueprint.route('/users/confirm/<token>')
def confirm_user(token):
    s = get_serializer()
    try:
        user_id = s.loads(token)
    except BadSignature:
        abort(404)

    user = User.query.get_or_404(user_id)
    if user.confirmed_email is True:
        flash("Your email has already been confirmed.")
        return redirect(url_for("pages.home"))
    user.confirm_email()
    flash("Your email has been confirmed!")
    return redirect(url_for("pages.home"))


@pages_blueprint.route('/users/resend-confirmation')
@login_required
@unconfirmed_email_required
def resend_confirmation_email():
    email_user_confirmation_link(current_user)
    flash("Resent confirmation email.")
    return redirect(url_for("pages.home"))


# ------------------
# email confirmation
# ------------------
# TODO: split into another file,
#       or gut functions into routing methods,
#       or leave as is? 

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = APP.config['SECRET_KEY']
    return URLSafeSerializer(secret_key)


def get_confirmation_link(user):
    s = get_serializer()
    token = s.dumps(user.id)
    return url_for('pages.confirm_user', token=token, _external=True)


def email_user_confirmation_link(user):
    subject = "Please confirm your email address"
    confirmation_link = get_confirmation_link(user)
    html = render_template('pages/emails/confirm.html',
                           confirmation_link=confirmation_link)
    send_email(user.email, subject, html)
