import json

import requests
from backend.config import MEDSENGER_KEY, MEDSENGER_HOST
from .exceptions import *
from datetime import date


def medsenger_login_user(login, password):
    data = {
        "login": login,
        "password": password,
        "api_key": MEDSENGER_KEY
    }

    answer = requests.post(MEDSENGER_HOST + "/api/research/auth", json=data).json()

    if answer['state'] == 'success':
        return answer['data']
    else:
        if 'User not found' in answer['error']:
            raise NotFound
        raise IncorrectPassword


def medsenger_get_scenarios(clinic):
    data = {
        "clinic_id": clinic.id,
        "api_key": MEDSENGER_KEY
    }

    answer = requests.post(MEDSENGER_HOST + "/api/research/scenarios", json=data).json()

    if answer['state'] == 'success':
        return answer['data']
    else:
        raise NotFound


@transaction
def medsenger_create_contract(user, patient_description, days):
    if not patient_description.get('name') or not patient_description.get('sex'):
        raise InsufficientData

    try:
        assert int(days) >= 1 and int(days) <= 365
    except:
        raise IncorrectDays

    if not check_email(patient_description.get('email')):
        raise IncorrectEmail

    try:
        birthday = date.fromisoformat(patient_description.get('birthday')).strftime('%d.%m.%Y')
    except:
        raise IncorrectBirthday

    data = {
        "clinic_id": user.clinic.id,
        "login": user.email,
        "days": days,
        "patient": {
            "name": patient_description.get('name'),
            "birthday": birthday,
            "sex": patient_description.get('sex'),
            "email": patient_description.get('email')
        },
        "api_key": MEDSENGER_KEY
    }

    print(json.dumps(data))

    answer = requests.post(MEDSENGER_HOST + "/api/research/create", json=data).json()

    print(answer)

    if answer['state'] == 'success':
        return answer['data']['contract_id']
    else:
        if 'Already exists' in answer['error']:
            raise MedsengerAlreadyExists

        raise InsufficientData
