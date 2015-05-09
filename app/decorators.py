from functools import wraps

from flask import flash, redirect, url_for
from flask.ext.login import current_user


def confirmed_email_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed_email is False:
            return redirect(url_for("users.need_confirm_email"))
        return func(*args, **kwargs)

    return decorated_function


def unconfirmed_email_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed_email is True:
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
