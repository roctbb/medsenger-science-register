import json

from sqlalchemy.orm.attributes import flag_modified

from backend.models import *
from .exceptions import *
from backend.helpers import *
from .comments import *
from sqlalchemy import Text


@transaction
def submit_form(doctor, patient, form, answers):
    if not doctor or not patient:
        raise NotFound("doctor / patient")

    if not form:
        raise NotFound("form")

    validate_form(form, answers)
    submission = create_submission(form, patient, doctor)

    if not patient.show_off_records:
        patient.show_off_records = []

    for part in form.parts:
        groups = extract_key(answers, part.id)
        for group_key, group in groups.items():
            for field in part.fields:
                if field.get('type') in ['subheader', 'header']:
                    continue

                answer = group.get(field.get('id'))
                category = find_category_by_code(field.get('category'))

                params = {
                    "group_key": group_key,
                    "part_id": part.id,
                    "question_id": field.get('id'),
                    "answer_text": answer,
                    "question_text": field.get('text')
                }

                if answer != None and category:
                    record = Record(patient_id=patient.id,
                                    category_id=category.id,
                                    submission_id=submission.id,
                                    value=answer,
                                    params=params)
                    db.session.add(record)

                    if field.get('params', {}).get('global_show_off'):
                        patient.show_off_records = list(
                            filter(lambda record: record['category_id'] != category.id, patient.show_off_records))

                        title = field.get('params', {}).get('global_show_off_title')
                        if not title:
                            title = category.name

                        patient.show_off_records.append({
                            "category_id": category.id,
                            "title": title,
                            "value": answer,
                            "transform": field.get('params', {}).get('global_show_off_transform')
                        })

                        flag_modified(patient, "show_off_records")

                if field.get('export_comment', False) and answer:
                    place_comment(form.project, patient, doctor, answer,
                                  description=f"{form.name}, {field.get('text')}", submission_id=submission.id)

    mark_updated(patient)

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
                if field.get('required') and field.get('id') not in group and (
                        not field.get('show_if') or group.get(field.get('show_if'))):
                    details.append((part.id, group_key, field.get('id')))
    if details:
        raise InsufficientData(json.dumps(details))


def get_saved_answers(form, patient):
    fields = []
    grouper = {}

    for part in form.parts:
        fields.extend(part.fields)

    saved_fields_ids = list(map(lambda f: f.get('id'), filter(lambda f: f.get("is_saved"), fields)))

    if saved_fields_ids:
        records = Record.query.filter(Record.patient_id == patient.id).filter(
            Record.params['question_id'].astext.in_(saved_fields_ids)).all()

        for record in records:
            qid = record.params['question_id']
            if qid in grouper:
                if record.created_on > grouper[qid].created_on:
                    grouper[qid] = record
            else:
                grouper[qid] = record

    return grouper.values()


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
    delete_submission_comments(old)
    new.created_on = old.created_on

    mark_updated(new.patient)


@transaction
def delete_submission_comments(submission):
    for comment in submission.comments:
        db.session.delete(comment)
