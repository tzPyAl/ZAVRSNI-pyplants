from flask import url_for
from flask_mail import Message
from pyplant import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Pyplant - Password Request Reset',
                  sender='noreply@pyplant.io', recipients=[user.email])
    msg.body = f'''Visit the following link to reset your password:
{url_for('users.reset_token', token=token, _external=True)}

This token will expire in 30 minutes.
'''
    mail.send(msg)
