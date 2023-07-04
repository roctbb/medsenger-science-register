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
