from backend.models import *


def find_answer_for_question(field, submission):
    for record in submission.records:
        if field['type'] in ('header', 'subheader'):
            continue
        if record.params['question_id'] == field['id']:
            return record.value

    return None

def get_answer_from_options(options, answer):
    for key, value in options.items():
        if answer == value:
            return key

    return answer


def get_header(form_parts):
    header = ["Пациент"]

    for part in form_parts:
        for field in part.fields:
            if field['type'] in ('header', 'subheader'):
                continue
            header.append(field['text'])

    return header

def generate_report_for_project(project):
    form_reports = []

    patients = project.patients
    forms = Form.query.filter_by(project_id=project.id, is_legacy=False).all()

    for form in forms:
        report = []
        parts = list(filter(lambda part: not part.repeatable, form.parts))

        header = get_header(parts)
        report.append(header)

        for patient in patients:
            row = [patient.name]

            all_form_submissions = list(sorted(form.submissions, key=lambda f: f.created_on))
            patient_submissions = list(
                filter(lambda s: not s.is_legacy and s.patient_id == patient.id, all_form_submissions))

            if not patient_submissions:
                report.append(row + [None] * (len(header) - 1))
                continue

            last_submission = patient_submissions[-1]

            for part in parts:
                for field in part.fields:
                    answer = find_answer_for_question(field, last_submission)

                    if 'options' in field['params']:
                        answer = get_answer_from_options(field['params']['options'], answer)

                    if answer:
                        row.append(answer)
                    else:
                        row.append(None)
            report.append(row)

        form_reports.append({
            "title": form.name,
            "report": report
        })

    return form_reports
