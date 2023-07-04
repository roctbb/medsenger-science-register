from backend.models import *
from .exceptions import *
from backend.helpers import *


def find_project_by_id_for_user(user, project_id):
    project = Project.query.get(project_id)

    if not project:
        raise NotFound

    if project not in user.clinic.projects:
        raise AccessDenied

    return project


def get_projects_for_user(user):
    if not user.clinic:
        return []
    return user.clinic.projects
