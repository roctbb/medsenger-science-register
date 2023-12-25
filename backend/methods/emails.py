from backend.manage import mail
from flask_mail import Message
from backend.config import EMAIL_SENDER, EMAIL_SENDER_NAME, HOST


def send_email(subject, message, recipient):
    msg = Message(subject=subject, html=message, recipients=[recipient], sender=(EMAIL_SENDER_NAME, EMAIL_SENDER))
    mail.send(msg)


def send_password_reset_email(user):
    subject = 'Восстановление пароля в регистре пациентов'
    recipient = user.email

    url = HOST + '/password/reset?key=' + user.password_reset_key
    message = f"Ссылка для восстановления пароля: <a href='{url}' target='_blank'>{url}</a>"

    send_email(subject, message, recipient)
