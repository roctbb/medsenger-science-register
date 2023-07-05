from backend.models import *
from .exceptions import *
from backend.helpers import *


def find_clinic_by_id(id):
    return Clinic.query.get(id)
