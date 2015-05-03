from flask.ext.mail import Message
from flask import current_app as APP

from app import mail


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=APP.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
