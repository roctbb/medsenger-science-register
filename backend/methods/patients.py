from backend.models import *
from .exceptions import *
from backend.helpers import *
from .projects import get_current_step


def get_patients_for_project(project):
    return filter(lambda x: not x.is_legacy, project.patients)


@transaction
def create_patient(user, name, sex, birthday, phone=None):
    if not name or not sex or not birthday:
        raise InsufficientData

    if find_patient_by_credentials(name, sex, birthday):
        raise AlreadyExists

    patient = Patient(name=name, sex=sex, birthday=birthday, phone=phone, doctor_id=user.id)
    db.session.add(patient)

    return patient


@transaction
def update_patient(patient, name, sex, birthday, phone=None):
    if not patient:
        raise NotFound

    if not name or not sex or not birthday:
        raise InsufficientData

    alternative = find_patient_by_credentials(name, sex, birthday)
    if alternative and alternative.id != patient.id:
        raise AlreadyExists

    patient.name = name
    patient.sex = sex
    patient.birthday = birthday
    patient.phone = phone

    return patient


def find_patient_by_credentials(name, sex, birthday):
    return Patient.query.filter_by(name=name, sex=sex, birthday=birthday).first()


def find_patient_by_id(patient_id):
    return Patient.query.get(patient_id)


@transaction
def assign_to_project(patient, project):
    if patient not in project.patients:
        project.patients.append(patient)
    else:
        raise AlreadyExists


@transaction
def save_contract(patient, project, doctor, contract_id):
    contract = Contract(patient_id=patient.id, project_id=project.id, id=contract_id, doctor_id=doctor.id)
    db.session.add(contract)

    return contract


def get_actual_contract_id(project, patient):
    contracts = list(filter(lambda c: c.project_id == project.id, patient.contracts))

    return contracts[-1].id if contracts else None


def load_project_data(patient, project):
    return {
        "contract_id": get_actual_contract_id(project, patient),
        "step": get_current_step(project, patient)
    }
