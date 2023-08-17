import json
import os
import base64

from backend.models import *
from .exceptions import *
from backend.helpers import *
from backend.config import STORAGE_PATH


@transaction
def upload_file(doctor, patient, project, file_dict):
    if not doctor or not patient:
        raise NotFound("doctor / patient")
    if not project:
        raise NotFound("project")

    file = create_file(file_dict, patient, doctor, project)

    return file


@transaction
def create_file(file_dict, patient, doctor, project):
    path = save_file(file_dict, patient.id)

    if not path:
        raise InsufficientData

    file = File(patient_id=patient.id, doctor_id=doctor.id, project_id=project.id,
                name=file_dict.get('name'), file_name=file_dict.get('file_name'),
                type=file_dict.get('type', 'plain/text'), path=path)

    db.session.add(file)
    return file


def save_file(file, patient_id):
    try:
        path = os.path.join(STORAGE_PATH, 'patient_{}'.format(str.zfill(str(patient_id), 4)))
        os.makedirs(path, exist_ok=True)

        bytes = file['base64'].encode('utf-8')
        with open(os.path.join(path, file['file_name']), 'wb') as file_to_save:
            decoded_data = base64.decodebytes(bytes)
            file_to_save.write(decoded_data)

        return path
    except Exception as e:
        raise InsufficientData


def get_patient_files(project, patient):
    if patient not in project.patients:
        raise NotInProject

    return File.query.filter_by(project_id=project.id, patient_id=patient.id).all()


def find_file_by_id(file_id):
    return File.query.get(file_id)


def get_file_data_by_id(file_id, doctor, patient, project):
    try:
        file = find_file_by_id(file_id)

        if not file:
            raise NotFound("file")

        if file.project_id != project.id or project not in doctor.clinic.projects or file.patient_id != patient.id:
            raise AccessDenied

        with open(os.path.join(file.path, file.name), 'rb') as binary_file:
            binary_file_data = binary_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            base64_message = base64_encoded_data.decode('utf-8')

            result = file.as_dict()
            result.update({'base64': base64_message})

            return result
    except Exception as e:
        return None


@transaction
def update_file(doctor, patient, project, file, new_name):
    if not doctor or not patient:
        raise NotFound("doctor / patient")
    if not project:
        raise NotFound("project")
    if not file:
        raise NotFound("file")
    file.name = new_name
    return file

@transaction
def delete_file_by_id(file_id, patient, doctor, project):
    file = find_file_by_id(file_id)

    if not file:
        raise NotFound("file")

    if file.project_id != project.id or project not in doctor.clinic.projects or file.patient_id != patient.id:
        raise AccessDenied

    File.query.filter_by(id=file_id).delete()
    try:
        path = os.path.join(STORAGE_PATH, 'patient_{}'.format(str.zfill(str(patient.id), 4)))
        if os.path.exists(path):
            for f in os.listdir(path):
                os.remove(os.path.join(path, f))

        return 'ok'
    except Exception as e:
        return None



