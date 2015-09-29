import datetime
from flask import (render_template, Blueprint, request, redirect, url_for, flash, current_app, session)
from flask.ext.login import (login_user, login_required,
                             current_user)
from ..extensions import db, twitter, user_datastore
from ..forms.users import SetUsernameForm
from ..models.users import User
from ..decorators import logout_required, unconfirmed_email_required
from flask.ext.security.confirmable import send_confirmation_instructions, confirm_user


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/confirm-email')
@login_required
@unconfirmed_email_required
def need_confirm_email():
    return render_template('users/confirm-email.html')


@users_blueprint.route('/users/resend-confirmation')
@login_required
@unconfirmed_email_required
def resend_confirmation_email():
    send_confirmation_instructions(current_user)
    flash("Resent confirmation email.")
    return redirect(url_for("pages.home"))


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
        new_user = user_datastore.create_user(username=new_user_username,
                                              twitter_username=twitter_username,
                                              is_oauth_user=True)
        db.session.add(new_user)
        db.session.commit()
        confirm_user(new_user)
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