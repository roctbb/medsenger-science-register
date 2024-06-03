import sys

from sqlalchemy.orm.attributes import flag_modified

from backend.manage import *
from backend.methods import mark_updated
from backend.models import Patient, FormSubmission, Form


# <количество исключений> <исключения> <формы>
with app.app_context():
    except_categories = [int(category_id) for category_id in sys.argv[2:(2 + int(sys.argv[1]))] if category_id.isdigit()]
    form_ids = [int(form_id) for form_id in sys.argv[(2 + int(sys.argv[1])):] if form_id.isdigit()]
    print(except_categories, form_ids)

    print('start extracting fields')
    forms = [db.session.get(Form, id) for id in form_ids]
    show_off_fields = []
    for form in forms:
        if form:
            for part in form.parts:
                show_off_fields += [{
                    'id': field['id'],
                    'title': field.get('params', {}).get('global_show_off_title'),
                    'transform': field.get('params', {}).get('global_show_off_transform', None)
                } for field in part.fields if field.get('params', {}).get('global_show_off')]

    show_off_field_ids = [f['id'] for f in show_off_fields]
    print('extracted fields count: ', len(show_off_fields))

    # Проходимся по пациентам
    print('start updating patients')
    patients = Patient.query.all()
    for patient in patients:
        if not patient.show_off_records:
            patient.show_off_records = []
        submissions = sorted(list(filter(lambda s: s.form_id in form_ids, patient.submissions)),
                             key=lambda s: s.updated_on)
        for submission in submissions:
            for record in submission.records:
                if record.params.get('question_id') in show_off_field_ids and record.category_id not in except_categories:
                    patient.show_off_records = list(filter(lambda rec: rec['category_id'] != record.category_id, patient.show_off_records))
                    show_off = [f for f in show_off_fields if f['id'] == record.params.get('question_id')]
                    patient.show_off_records.append({
                            "category_id": record.category_id,
                            "title": show_off[0]['title'],
                            "value": record.value,
                            "transform": show_off[0]['transform']
                        })
                    flag_modified(patient, "show_off_records")

        mark_updated(patient)
    db.session.commit()
print('all patients are updated')