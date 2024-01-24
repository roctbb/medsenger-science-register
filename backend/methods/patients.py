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
def mark_updated(patient):
    patient.updated_on = datetime.now()


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

    mark_updated(patient)

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


def get_last_visit_time(user, project, patient):
    request = PatientVisitedTime.query.filter_by(user_id=user.id, patient_id=patient.id, project_id=project.id).first()

    if not request:
        return None

    return request.visited_on


def load_project_data(patient, project, user):
    last_visit_time = get_last_visit_time(user, project, patient)

    return {
        "contract_id": get_actual_contract_id(project, patient),
        "step": get_current_step(project, patient),
        "last_visited_time": last_visit_time.isoformat() if last_visit_time else None
    }


@transaction
def set_last_visited_time(user, patient, project):
    request = PatientVisitedTime.query.filter_by(user_id=user.id, patient_id=patient.id, project_id=project.id).first()

    if not request:
        request = PatientVisitedTime(user_id=user.id, patient_id=patient.id, project_id=project.id)
        db.session.add(request)

    request.visited_on = datetime.now()
