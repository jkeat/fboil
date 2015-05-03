from flask.ext.mail import Message

from app import mail


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender="unitaryans@gmail.com"  # TODO app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
