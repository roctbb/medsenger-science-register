from backend.models import *
from .exceptions import *
from backend.helpers import *


@transaction
def create_user(email, password, name, clinic):
    if not email or not password or not name or not clinic:
        raise InsufficientData

    if find_user_by_email(email):
        raise AlreadyExists

    user = User(email=email, password=hash(password), name=name, clinic_id=clinic.id)
    db.session.add(user)

    return user


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def find_user_by_id(id):
    return User.query.get(id)


@transaction
def change_user_password(user, new_password):
    user.password = hash(new_password)
