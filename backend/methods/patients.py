from backend.models import *
from .exceptions import *
from backend.helpers import *


@transaction
def create_patient(name, sex, birthday):
    if not name or not sex or not birthday:
        raise InsufficientData

    if find_patient_by_credentials(name, sex, birthday):
        return AlreadyExists

    patient = Patient(name=name, sex=sex, birthday=birthday)
    db.session.add(patient)

    return patient


def find_patient_by_credentials(name, sex, birthday):
    return Patient.query.filter_by(name=name, sex=sex, birthday=birthday).first()


@transaction
def assign_to_project(patient, project):
    if patient not in project.patients:
        project.patients.append(patient)
    else:
        raise AlreadyExists
