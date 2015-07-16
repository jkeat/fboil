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


users_blueprint = Blueprint('users', __name__)



# =============================================
# =============================================

import os

from flask import session

from flask_oauth import OAuth
oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
    consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"]
)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@users_blueprint.route('/twitter-login')
def twitter_login():
    if session.has_key('twitter_token'):  # check if 'already logged in'
        del session['twitter_token']
    return twitter.authorize()  # (redirect url is hardcoded online b/c
                                # giving a localhost url wasn't working)

    # return twitter.authorize(callback=url_for('users.oauth_authorized',
    #     next=request.args.get('next') or request.referrer or None))


@users_blueprint.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('pages.home')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


# =============================================
# =============================================



@users_blueprint.route('/login', methods=['GET', 'POST'])
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


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("pages.home"))


@users_blueprint.route('/signup', methods=['GET', 'POST'])
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


@users_blueprint.route('/users/confirm/<token>')
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


@users_blueprint.route('/users/resend-confirmation')
@login_required
@unconfirmed_email_required
def resend_confirmation_email():
    email_user_confirmation_link(current_user)
    flash("Resent confirmation email.")
    return redirect(url_for("pages.home"))


@users_blueprint.route('/confirm-email')
@login_required
@unconfirmed_email_required
def need_confirm_email():
    return render_template('users/confirm-email.html')


@users_blueprint.route('/forgot', methods=['GET', 'POST'])
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


@users_blueprint.route('/users/reset-password/<token>', methods=["GET", "POST"])
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

def email_user_confirmation_link(user):
    """
    Used initially on signup and when user resends confirm email.
    """
    token = serializer.serialize_data(user.id)
    confirmation_link = url_for('users.confirm_user',
                                token=token, _external=True)

    subject = "Please confirm your email address"
    html = render_template('users/emails/confirm.html',
                           confirmation_link=confirmation_link)
    send_email(user.email, subject, html)
