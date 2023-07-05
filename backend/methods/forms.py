from backend.models import *
from .exceptions import *
from backend.helpers import *


@transaction
def submit_form(doctor, patient, form, answers):
    if not doctor or not patient:
        raise NotFound("doctor / patient")

    if not form:
        raise NotFound("form")

    validate_form(form, answers)

    submission = create_submission(form, patient, doctor)

    for part in form.parts:
        for field in part.fields:
            answer = answers.get(field.get('id'))
            category = find_category_by_code(field.get('category'))

            params = {
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

    return FormSubmission.query.filter_by(project_id=project.id, patient_id=patient.id).all()


def validate_form(form, answers):
    for part in form.parts:
        for field in part.fields:
            if field.get('required') and field.get('id') not in answers:
                raise InsufficientData(field.get('id'))


def find_form_by_id(form_id):
    return Form.query.get(form_id)


def find_category_by_code(category_code):
    return RecordCategory.query.filter_by(code=category_code).first()
