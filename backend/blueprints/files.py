from flask import Blueprint, request
from backend.methods import *

file_blueprint = Blueprint('files', __name__)


@file_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/files', methods=['get'])
@creates_response
@requires_user
def get_files(user, project_id, patient_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    patient_files = get_patient_files(project, patient)

    return as_dict(patient_files)


@file_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/files', methods=['post'])
@creates_response
@requires_user
def add_file(user, project_id, patient_id):
    data = request.json

    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    file = upload_file(user, patient, project, data.get('file'))

    return file.as_dict()


@file_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/files/<int:file_id>', methods=['put'])
@creates_response
@requires_user
def edit_file(user, project_id, patient_id, file_id):
    data = request.json

    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)
    file = find_file_by_id(file_id)

    new_file = update_file(user, patient, project, file, data.get('new_file_name'))

    return new_file.as_dict()


@file_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/files/<int:file_id>', methods=['get'])
@creates_response
@requires_user
def get_file(user, project_id, patient_id, file_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    full_file = get_file_data_by_id(file_id, user, patient, project)

    return full_file


@file_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/files/<int:file_id>', methods=['DELETE'])
@creates_response
@requires_user
def delete_file(user, project_id, patient_id, file_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    delete_file_by_id(file_id, patient, user, project)

    return 'ok'
