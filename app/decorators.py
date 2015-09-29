from functools import wraps

from flask import flash, redirect, url_for
from flask.ext.login import current_user  # TODO: flask.ext.security.core import current_user


def confirmed_email_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous():
            # Will only happen during tests
            # where login_required is waved
            if current_user.is_anonymous():
                print "In decorator, user IS anonymous"
            else:
                print "In decorator, user is NOT anonymous"
            return redirect(url_for("users.need_confirm_email"))
        if not current_user.confirmed_at:
            print "In decorator, user's email IS confirmed"
            return redirect(url_for("users.need_confirm_email"))
        else:
            print "In decorator, user's email is NOT confirmed"
        return func(*args, **kwargs)

    return decorated_function


def unconfirmed_email_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous():
            # Will only happen during tests,
            # where login_required is waved
            return redirect(url_for("security.login"))
        if current_user.confirmed_at:
            flash("Your email has already been confirmed.")
            return redirect(url_for("pages.home"))
        return func(*args, **kwargs)

    return decorated_function


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated():
            return redirect(url_for("pages.home"))
        return func(*args, **kwargs)

    return decorated_function
