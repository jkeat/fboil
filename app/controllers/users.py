import datetime
from flask import (render_template, Blueprint, request, abort,
                   redirect, url_for, flash, current_app, session)
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from itsdangerous import BadSignature
from ..extensions import serializer, db, twitter
from ..forms.users import (RegisterForm, LoginForm, ForgotPasswordForm,
                           ResetPasswordForm, SetUsernameForm)
from ..models.users import User
from ..decorators import unconfirmed_email_required, logout_required
from ..utils import send_email, email_user_confirmation_link


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()

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
    login_user(user)
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
            login_user(user)
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


@users_blueprint.route('/twitter-login')
@logout_required
def twitter_login():
    if session.has_key('twitter_token'):  # check if 'already logged in'
        del session['twitter_token']

    # if os.environ.get('APP_SETTINGS') == "config.ProductionConfig":
    #     return twitter.authorize(callback=url_for('users.oauth_authorized',
    #         next=request.args.get('next')))
    # else:
    #     return twitter.authorize()

    return twitter.authorize()  # That ^ isn't working. Can't get Twitter
                                # to recognize it's being given a callback.
                                # The callback is just hardcoded on apps.twitter.com.
                                # (One app for dev w/ 127.0.0.1:5000/oauth-authorized
                                # as the callback, one for production w/
                                # https://fboil.herokuapp.com/oauth-authorized as the
                                # callback. Set config vars on Heroku to dif't API keys.)


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

    twitter_username = resp['screen_name']
    session['twitter_user'] = twitter_username

    twitter_user_response = twitter.get('users/show.json', data={"screen_name": twitter_username})
    twitter_user_data = twitter_user_response.data

    this_user = User.query.filter_by(twitter_username=twitter_username).first()
    if this_user:
        login_user(this_user)
        return redirect(next_url)
    else:
        new_user_username = User.make_unique_username(twitter_username)
        new_user = User(username=new_user_username, twitter_username=twitter_username, is_oauth_user=True)
        new_user.confirmed_email = True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('users.set_username', next=next_url))


@users_blueprint.route('/set-username', methods=['GET', 'POST'])
@login_required
def set_username():
    if not current_user.is_oauth_user:
        return redirect(url_for('pages.home'))

    SECONDS_TO_CHANGE = current_app.config['SECONDS_TO_CHANGE_USERNAME']
    # User gets certain amoun of time after oauth signup to change username
    if (datetime.datetime.now() - current_user.created_on) > datetime.timedelta(0, SECONDS_TO_CHANGE, 0):
        flash("It's too late for that, sorry! You're stuck with the username {0}".format(current_user.username))
        return redirect(url_for('pages.home'))

    form = SetUsernameForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('users/forms/set-username.html', form=form)
        else:
            form.set_username(current_user.id)
            next_url = request.args.get('next') or url_for('pages.home')
            return redirect(next_url)

    elif request.method == 'GET':
        return render_template('users/forms/set-username.html', form=form)
