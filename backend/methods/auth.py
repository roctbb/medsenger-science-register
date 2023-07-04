from datetime import datetime, timedelta
from backend.models import *
from .exceptions import *
from backend.helpers import *
from .users import *
from backend.models import *
from secrets import token_hex


def authorize_by_credentials(email, password):
    user = find_user_by_email(email)

    if not user:
        raise NotFound

    if not check_password(user, password):
        raise IncorrectPassword

    return user, create_token(user)


def authorize(user):
    return create_token(user)


def check_password(user, password):
    return user.password == hash(password)


def find_user_by_token(token):
    if not token:
        raise NoToken

    token = UserToken.query.filter_by(token=token).first()

    if not token:
        raise IncorrectToken

    if token.expire_on < datetime.now():
        raise ExpiredToken

    return token.user


@transaction
def create_token(user):
    token = UserToken(user_id=user.id)
    token.expire_on = datetime.now() + timedelta(days=7)
    token.token = token_hex(32)

    db.session.add(token)
    return token
