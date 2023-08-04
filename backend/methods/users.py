from secrets import token_hex

from backend.models import *
from .exceptions import *
from backend.helpers import *


@transaction
def create_user(email, name, clinic, specialties=(), password=None):
    if not email or not name or not clinic:
        raise InsufficientData

    if find_user_by_email(email):
        raise AlreadyExists

    user = User(email=email, name=name, clinic_id=clinic.id, specialties=specialties)

    if password:
        set_password(user, password)
    else:
        set_activation_key(user)

    db.session.add(user)

    return user


@transaction
def set_password(user, password):
    user.password = hash(password)
    user.activation_key = None


@transaction
def set_activation_key(user):
    user.activation_key = token_hex(16)


@transaction
def activate_user(user, password):
    if not password or len(password) < 8:
        raise InsufficientData

    user.password = hash(password)
    user.activation_key = None

    return user


def find_user_by_email(email):
    return User.query.filter_by(email=email.lower()).first()


def find_user_by_activation_key(key):
    return User.query.filter_by(activation_key=key).first()


def find_user_by_id(id):
    return User.query.get(id)


@transaction
def change_user_password(user, new_password):
    user.password = hash(new_password)
