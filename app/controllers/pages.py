from flask import (render_template, Blueprint, request, session,
                   redirect, url_for, flash, abort)
from flask import current_app as APP
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from itsdangerous import (URLSafeSerializer, URLSafeTimedSerializer,
                          BadSignature)
from app.forms import *
from app.models import *
from app.decorators import confirmed_email_required, unconfirmed_email_required
from app.email import send_email

pages_blueprint = Blueprint('pages', __name__)

# TODO: blueprint for 'users'?
# TODO: rename 'pages_blueprint' > 'pages'?


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
    if current_user.is_authenticated():  # TODO: logout required decorator
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
    if current_user.is_authenticated():  # TODO: logout required decorator
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
    try:
        user_id = load_token(token)
    except BadSignature:
        abort(404)

    user = User.query.get_or_404(user_id)
    if user.confirmed_email is True:
        flash("Your email has already been confirmed.")
        return redirect(url_for("pages.home"))
    user.confirm_email()
    flash("Congrats! Your accounthas been activated.")
    return redirect(url_for("pages.home"))


@pages_blueprint.route('/users/resend-confirmation')
@login_required
@unconfirmed_email_required
def resend_confirmation_email():
    email_user_confirmation_link(current_user)
    flash("Resent confirmation email.")
    return redirect(url_for("pages.home"))


@pages_blueprint.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated():  # TODO: logout required decorator
        return redirect(url_for("pages.home"))

    form = ForgotPasswordForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('pages/forms/forgot-password.html',
                                   form=form)
        else:
            email_user_password_reset_link(form.email.data)
            flash("Password reset link emailed.")
            return redirect(url_for('pages.forgot_password'))
    elif request.method == 'GET':
        return render_template('pages/forms/forgot-password.html', form=form)


@pages_blueprint.route('/users/reset-password/<token>',
                       methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()

    if request.method == "POST":
        if not form.validate():
            return render_template('pages/forms/reset-password.html',
                                   form=form)
        else:
            # get user from encoded email token in url
            try:
                email = load_timed_token(token)
            except BadSignature:
                abort(404)
            user = User.query.filter_by(email=email).first()
            if user is None:
                abort(404)

            # then change their password to the new one
            form.change_password(user)
            flash("Password changed successfully!")

            return redirect(url_for('pages.login'))

    elif request.method == "GET":
        try:
            email = load_timed_token(token)
        except BadSignature:
            abort(404)
        user = User.query.filter_by(email=email).first()
        if user is None:
            abort(404)
        return render_template('pages/forms/reset-password.html', form=form)


# =============================
# === non-routing functions ===
# =============================

# TODO: split these into another file,
#       or gut functions into routing methods,
#       or leave as is?


# ------------------
# serializers # TODO: make a class
# ------------------

def get_serializer():
    secret_key = APP.config['SECRET_KEY']
    return URLSafeSerializer(secret_key)


def get_timed_serializer():
    secret_key = APP.config['SECRET_KEY']
    return URLSafeTimedSerializer(secret_key)


def serialize_data(data):
    s = get_serializer()
    return s.dumps(data, salt=APP.config['SECURITY_PASSWORD_SALT'])


def serialize_timed_data(data):
    s = get_timed_serializer()
    return s.dumps(data, salt=APP.config['SECURITY_PASSWORD_SALT'])


def load_token(token):
    s = get_serializer()
    salt = APP.config['SECURITY_PASSWORD_SALT']
    return s.loads(token, salt=salt)


def load_timed_token(token, expiration=3600):
    s = get_timed_serializer()
    salt = APP.config['SECURITY_PASSWORD_SALT']
    return s.loads(token, salt=salt, max_age=expiration)


# ------------------
# email confirmation  # TODO: used twice
# ------------------

def email_user_confirmation_link(user):
    token = serialize_data(user.id)
    confirmation_link = url_for('pages.confirm_user',
                                token=token, _external=True)

    subject = "Please confirm your email address"
    html = render_template('pages/emails/confirm.html',
                           confirmation_link=confirmation_link)
    send_email(user.email, subject, html)


# --------------
# password reset  # TODO: used once
# --------------

def email_user_password_reset_link(email):
    token = serialize_timed_data(email)
    reset_link = url_for('pages.reset_password', token=token, _external=True)
    subject = "Your password reset link"
    html = render_template('pages/emails/reset_password.html',
                           reset_link=reset_link)
    send_email(email, subject, html)
