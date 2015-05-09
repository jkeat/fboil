from flask import (render_template, Blueprint, request, abort,
                   redirect, url_for, flash)
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from itsdangerous import BadSignature
from ..extensions import serializer
from ..forms.users import (RegisterForm, LoginForm, ForgotPasswordForm,
                           ResetPasswordForm)
from ..models.users import User
from ..decorators import (confirmed_email_required,
                          unconfirmed_email_required, logout_required)
from ..utils import send_email


users = Blueprint('users', __name__)


@users.route('/confirm-email')
@login_required
@unconfirmed_email_required
def need_confirm_email():
    return render_template('users/confirm-email.html')


@users.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            return render_template('users/forms/login.html', form=form)
        else:
            user = form.get_user()
            login_user(user, remember=True)
            redirect_page = request.args.get("next", url_for("pages.home"))
            return redirect(redirect_page)

    elif request.method == 'GET':
        return render_template('users/forms/login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("pages.home"))


@users.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('users/forms/register.html', form=form)
        else:
            new_user = form.create_user()
            login_user(new_user, remember=True)

            email_user_confirmation_link(new_user)

            flash("Account created successfully! Please confirm your email.")
            return redirect(url_for("pages.home"))
    elif request.method == "GET":
        return render_template('users/forms/register.html', form=form)


@users.route('/users/confirm/<token>')
def confirm_user(token):
    try:
        user_id = serializer.load_token(token)
    except BadSignature:
        abort(404)

    user = User.query.get_or_404(user_id)
    if user.confirmed_email is True:
        flash("Your email has already been confirmed.")
        return redirect(url_for("pages.home"))
    user.confirm_email()
    flash("Congrats! Your account has been activated.")
    return redirect(url_for("pages.home"))


@users.route('/users/resend-confirmation')
@login_required
@unconfirmed_email_required
def resend_confirmation_email():
    email_user_confirmation_link(current_user)
    flash("Resent confirmation email.")
    return redirect(url_for("pages.home"))


@users.route('/forgot', methods=['GET', 'POST'])
@logout_required
def forgot_password():
    form = ForgotPasswordForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('users/forms/forgot-password.html',
                                   form=form)
        else:
            email = form.email.data
            token = serializer.serialize_timed_data(email)
            reset_link = url_for(
                'users.reset_password', token=token, _external=True)
            subject = "Your password reset link"
            html = render_template('users/emails/reset_password.html',
                                   reset_link=reset_link)
            send_email(email, subject, html)
            flash("Password reset link emailed.")
            return redirect(url_for('users.login'))
    elif request.method == 'GET':
        return render_template('users/forms/forgot-password.html', form=form)


@users.route('/users/reset-password/<token>', methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()

    if request.method == "POST":
        if not form.validate():
            return render_template('users/forms/reset-password.html',
                                   form=form)
        else:
            # get user from encoded email token in url
            try:
                email = serializer.load_timed_token(token)
            except BadSignature:
                abort(404)
            user = User.query.filter_by(email=email).first()
            if user is None:
                abort(404)

            # then change their password to the new one
            form.change_password(user)
            flash("Password changed successfully!")

            return redirect(url_for('users.login'))

    elif request.method == "GET":
        try:
            email = serializer.load_timed_token(token)
        except BadSignature:
            abort(404)
        user = User.query.filter_by(email=email).first()
        if user is None:
            abort(404)
        return render_template('users/forms/reset-password.html', form=form)


# =============================
# === non-routing functions ===
# =============================

# TODO: put these into another file,
#       or gut functions into routing methods,
#       or leave as is?


# ------------------
# email confirmation  # TODO: is used twice
# ------------------

def email_user_confirmation_link(user):
    token = serializer.serialize_data(user.id)
    confirmation_link = url_for('users.confirm_user',
                                token=token, _external=True)

    subject = "Please confirm your email address"
    html = render_template('users/emails/confirm.html',
                           confirmation_link=confirmation_link)
    send_email(user.email, subject, html)
