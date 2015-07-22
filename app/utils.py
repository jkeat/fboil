from flask.ext.mail import Message
from flask import current_app, url_for, render_template
from .extensions import mail, serializer


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


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
