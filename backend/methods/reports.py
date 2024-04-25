from backend.models import *
import pandas as pd
from openpyxl.workbook.child import INVALID_TITLE_REGEX


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


def get_header_for_part(part):
    header = []
    for field in part.fields:
        if field['type'] in ('header', 'subheader'):
            continue
        header.append(field['text'])
    return header


def get_header(form_parts):
    header = []

    for part in form_parts:
        header += get_header_for_part(part)

    return header


def save_to_excel(reports):
    reports = list(map(lambda report: {
        "title": INVALID_TITLE_REGEX.sub(' ', report['title']),
        "dataframe": pd.DataFrame(report['report'][1:], columns=report['report'][0])
    }, reports))

    with pd.ExcelWriter("backend/report.xlsx") as writer:
        for report in reports:
            report["dataframe"].to_excel(writer, sheet_name=report['title'], index=False)

    return "report.xlsx"


def generate_common_reports(patients, forms):
    form_reports = []

    for form in forms:
        report = []
        parts = list(filter(lambda part: not part.repeatable, form.parts))

        header = ["Пациент", "Дата заполнения"] + get_header(parts)
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
            row.append(last_submission.created_on)

            for part in parts:
                for field in part.fields:
                    if field['type'] in ('header', 'subheader'):
                        continue

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


def get_part_submissions(submissions, part):
    part_submissions = {}

    for submission in submissions:
        for record in submission.records:
            if record.params.get('part_id') == part.id:
                group_key = record.params.get('group_key')
                question_id = record.params.get('question_id')
                answer = record.value

                if group_key not in part_submissions:
                    part_submissions[group_key] = {'created_on': submission.created_on}

                part_submissions[group_key][question_id] = answer

    return part_submissions


def generate_additional_reports(patients, forms):
    form_reports = []

    for form in forms:
        parts = list(filter(lambda part: part.repeatable, form.parts))
        all_form_submissions = list(sorted(form.submissions, key=lambda f: f.created_on))

        for part in parts:
            header = ["Пациент", "Дата заполнения"] + get_header_for_part(part)
            report = [header]

            for patient in patients:
                patient_submissions = list(
                    filter(lambda s: not s.is_legacy and s.patient_id == patient.id, all_form_submissions))

                part_submissions = get_part_submissions(patient_submissions, part)

                for submission in part_submissions.values():

                    row = [patient.name, submission['created_on']]

                    for field in part.fields:
                        if field['type'] in ('header', 'subheader'):
                            continue

                        answer = submission.get(field['id'])

                        if answer:
                            if 'options' in field['params']:
                                answer = get_answer_from_options(field['params']['options'], answer)
                            row.append(answer)
                        else:
                            row.append(None)
                    report.append(row)

            form_reports.append({
                "title": part.name,
                "report": report
            })

    return form_reports


def generate_report_for_project(project):
    patients = list(sorted(project.patients, key=lambda p: p.name))
    forms = Form.query.filter_by(project_id=project.id, is_legacy=False).all()

    return generate_common_reports(patients, forms) + generate_additional_reports(patients, forms)
