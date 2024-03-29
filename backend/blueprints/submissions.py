from flask import Blueprint, request
from backend.methods import *

submission_blueprint = Blueprint('submissions', __name__)


@submission_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/submissions', methods=['get'])
@creates_response
@requires_user
def get_submissions(user, project_id, patient_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    submissions = get_patient_submissions(project, patient)

    return as_dict(submissions)


@submission_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/visited', methods=['get'])
@creates_response
@requires_user
def mark_visited(user, project_id, patient_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    set_last_visited_time(user, patient, project)

    return {}


@submission_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/submissions', methods=['post'])
@creates_response
@requires_user
def add_submission(user, project_id, patient_id):
    data = request.json

    print(gts(), "Got submission", data)

    form_id = data.get('form_id')
    answers = data.get('answers')

    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)
    form = find_form_by_id(form_id)

    submission = submit_form(user, patient, form, answers)
    set_last_visited_time(user, patient, project)

    return submission.as_dict()


@submission_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/submissions/<int:submission_id>',
                            methods=['put'])
@creates_response
@requires_user
def edit_submission(user, project_id, patient_id, submission_id):
    data = request.json

    form_id = data.get('form_id')
    answers = data.get('answers')

    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)
    form = find_form_by_id(form_id)

    new_submission = submit_form(user, patient, form, answers)
    legacy_submission = find_submission_by_id(submission_id)

    replace_submission(legacy_submission, new_submission)
    set_last_visited_time(user, patient, project)

    return new_submission.as_dict()


@submission_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/submissions/<int:submission_id>',
                            methods=['delete'])
@creates_response
@requires_user
def remove_submission(user, project_id, patient_id, submission_id):
    project = find_project_by_id_for_user(user, project_id)
    legacy_submission = find_submission_by_id(submission_id)

    mark_legacy(legacy_submission)
    delete_submission_comments(legacy_submission)

    return None


@submission_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/saved/<int:form_id>',
                            methods=['get'])
@creates_response
@requires_user
def get_latest_answers(user, project_id, patient_id, form_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)
    form = find_form_by_id(form_id)

    return as_dict(get_saved_answers(form, patient))
