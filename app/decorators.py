from functools import wraps

from flask import flash, redirect, url_for
from flask.ext.login import current_user


def activated_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed_email is False:
            flash("Confirm your account first!")
            return redirect(url_for("pages.home"))
        return func(*args, **kwargs)

    return decorated_function
