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


def check_has_submission(patient, form_id):
    return len(list(filter(lambda submission: submission.form_id == form_id, patient.submissions))) > 0


def check_step_criteria(patient, step):
    for group in step.get('conditions', []):
        if all(check_has_submission(patient, form_id) for form_id in group):
            return True

    return False


def get_current_step(project, patient):
    if not project.steps:
        return None

    last_undone_step_index = None
    for i, step in enumerate(reversed(project.steps)):
        if not check_step_criteria(patient, step):
            last_undone_step_index = i
            break

    if last_undone_step_index == None:
        return "Завершено"
    else:
        return project.steps[last_undone_step_index].get('title')
