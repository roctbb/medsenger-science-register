from flask import Blueprint, request
from backend.methods import *

projects_blueprint = Blueprint('projects', __name__)


@projects_blueprint.route('/projects', methods=['get'])
@creates_response
@requires_user
def get_projects(user):
    return as_dict(get_projects_for_user(user))


@projects_blueprint.route('/project/<int:project_id>', methods=['get'])
@creates_response
@requires_user
def get_project(user, project_id):
    project = find_project_by_id_for_user(user, project_id)
    return project.as_dict()


@projects_blueprint.route('/project/<int:project_id>/patients', methods=['get'])
@creates_response
@requires_user
def get_patients(user, project_id):
    project = find_project_by_id_for_user(user, project_id)
    patients = get_patients_for_project(project)
    patients_descriptions = list(
        sorted(as_dict(patients, load_project_data, project, user), key=lambda p: p['name']))

    return patients_descriptions


@projects_blueprint.route('/project/<int:project_id>/patients', methods=['post'])
@creates_response
@requires_user
def add_patient(user, project_id):
    project = find_project_by_id_for_user(user, project_id)

    data = request.json
    contract_id = None
    if data.get('medsenger_contract') == True:
        contract_id = medsenger_create_contract(user, data, data.get('days'))

    try:
        patient = create_patient(user, data.get('name'), data.get('sex'), data.get('birthday'), data.get('phone'),
                                 data.get('email'))
    except AlreadyExists:
        patient = find_patient_by_credentials(data.get('name'), data.get('sex'), data.get('birthday'))
        patient = update_patient(patient, data.get('name'), data.get('sex'), data.get('birthday'), data.get('phone'),
                                 data.get('email'))

    assign_to_project(patient, project)

    if contract_id:
        save_contract(patient, project, user, contract_id)

    set_last_visited_time(user, patient, project)

    return patient.as_dict(load_project_data(patient, project, user))


@projects_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>', methods=['put'])
@creates_response
@requires_user
def edit_patient(user, project_id, patient_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    if patient not in project.patients:
        raise NotInProject

    data = request.json

    patient = update_patient(patient, data.get('name'), data.get('sex'), data.get('birthday'), data.get('phone'),
                             data.get('email'))

    contract_id = None
    if data.get('medsenger_contract') == True and not patient.contracts:
        contract_id = medsenger_create_contract(user, data, data.get('days'))

    if contract_id:
        save_contract(patient, project, user, contract_id)

    set_last_visited_time(user, patient, project)

    return patient.as_dict(load_project_data(patient, project, user))


@projects_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>', methods=['get'])
@creates_response
@requires_user
def get_patient(user, project_id, patient_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    if patient not in project.patients:
        raise NotInProject

    return patient.as_dict(load_project_data(patient, project, user))


@projects_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>', methods=['delete'])
@creates_response
@requires_user
def remove_patient(user, project_id, patient_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    if patient not in project.patients:
        raise NotInProject

    mark_legacy(patient)

    return None
