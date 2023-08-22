import json

from backend.models import *
from .exceptions import *
from backend.helpers import *
from .comments import *


@transaction
def submit_form(doctor, patient, form, answers):
    if not doctor or not patient:
        raise NotFound("doctor / patient")

    if not form:
        raise NotFound("form")

    validate_form(form, answers)

    submission = create_submission(form, patient, doctor)

    for part in form.parts:
        groups = extract_key(answers, part.id)

        for group_key, group in groups.items():
            for field in part.fields:
                answer = group.get(field.get('id'))
                category = find_category_by_code(field.get('category'))

                params = {
                    "group_key": group_key,
                    "part_id": part.id,
                    "question_id": field.get('id'),
                    "answer_text": answer,
                    "question_text": field.get('text')
                }

                if answer and category:
                    record = Record(patient_id=patient.id,
                                    category_id=category.id,
                                    submission_id=submission.id,
                                    value=answer,
                                    params=params)
                    db.session.add(record)

                if field.get('export_comment', False) and answer:
                    place_comment(form.project, patient, doctor, answer,
                                  description=f"{form.name}, {field.get('text')}", submission_id=submission)

    return submission


def find_question_for_answer(field, answer):
    field_type = field.get('type')
    if field_type == 'radio' or field_type == 'select':
        for question, variant in field.get('params', {}).get('options'):
            if variant == answer:
                return question

    if field_type == 'checkbox':
        options = field.get('params', {}).get('options')
        if answer == options['true']:
            return 'Да'
        else:
            return 'Нет'

    return answer


@transaction
def create_submission(form, patient, doctor):
    submission = FormSubmission(form_id=form.id, patient_id=patient.id, doctor_id=doctor.id, project_id=form.project_id)
    db.session.add(submission)
    return submission


def get_patient_submissions(project, patient):
    if patient not in project.patients:
        raise NotInProject

    return FormSubmission.query.filter_by(is_legacy=False, project_id=project.id, patient_id=patient.id).all()


def extract_key(data, key):
    return data.get(key, data.get(str(key), {}))


def validate_form(form, answers):
    details = []

    for part in form.parts:
        if not part.repeatable and not extract_key(answers, part.id):
            raise InsufficientData()

        for group_key, group in extract_key(answers, part.id).items():
            for field in part.fields:
                if field.get('required') and field.get('id') not in group:
                    details.append((part.id, group_key, field.get('id')))
    if details:
        raise InsufficientData(json.dumps(details))


def find_form_by_id(form_id):
    return Form.query.get(form_id)


def find_submission_by_id(submission_id):
    return FormSubmission.query.get(submission_id)


@transaction
def mark_legacy(object):
    object.is_legacy = True


def find_category_by_code(category_code):
    return RecordCategory.query.filter_by(code=category_code).first()


@transaction
def replace_submission(old, new):
    mark_legacy(old)

    for comment in old.commets:
        db.session.delete(comment)

    new.created_on = old.created_on
