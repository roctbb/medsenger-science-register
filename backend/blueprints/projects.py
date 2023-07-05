from flask import Blueprint, request
from backend.methods import *

projects_blueprint = Blueprint('projects', __name__)


@projects_blueprint.route('/projects', methods=['get'])
@creates_response
@requires_user
def get_projects(user):
    return as_dict(get_projects_for_user(user))


@projects_blueprint.route('/project/<int:project_id>/patients', methods=['get'])
@creates_response
@requires_user
def get_patients(user, project_id):
    project = find_project_by_id_for_user(user, project_id)

    return as_dict(project.patients)


@projects_blueprint.route('/project/<int:project_id>/patients', methods=['post'])
@creates_response
@requires_user
def add_patient(user, project_id):
    project = find_project_by_id_for_user(user, project_id)

    data = request.json

    try:
        patient = create_patient(data.get('name'), data.get('sex'), data.get('birthday'))
    except AlreadyExists:
        patient = find_patient_by_credentials(data.get('name'), data.get('sex'), data.get('birthday'))

    assign_to_project(patient, project)

    return patient.as_dict()


@projects_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>', methods=['put'])
@creates_response
@requires_user
def edit_patient(user, project_id, patient_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    if patient not in project.patients:
        raise NotInProject

    data = request.json

    patient = update_patient(patient, data.get('name'), data.get('sex'), data.get('birthday'))

    return patient.as_dict()
