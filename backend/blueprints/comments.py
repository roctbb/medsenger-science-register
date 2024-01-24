from flask import Blueprint, request
from backend.methods import *

comments_blueprint = Blueprint('comments', __name__)


@comments_blueprint.route('/project/<int:project_id>/patients/<int:patient_id>/comments', methods=['post'])
@creates_response
@requires_user
def add_comment(user, project_id, patient_id):
    project = find_project_by_id_for_user(user, project_id)
    patient = find_patient_by_id(patient_id)

    if patient not in project.patients:
        raise NotInProject

    data = request.json

    comment = place_comment(project, patient, user, data.get('text'))
    set_last_visited_time(user, patient, project)

    return comment.as_dict()
