from backend.models import *
from .exceptions import *
from backend.helpers import *


@transaction
def create_patient(name, sex, birthday):
    if not name or not sex or not birthday:
        raise InsufficientData

    user = Patient(name=name, sex=sex, birthday=birthday)
    db.session.add(user)

    return user