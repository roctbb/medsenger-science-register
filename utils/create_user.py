from backend.methods import *
from backend.server import app

try:
    email = input("email:")
    password = input("password:")
    name = input("name:")
    clinic_id = input("clinic_id:")
    specialty = input('specialty:')

    with app.app_context():
        clinic = find_clinic_by_id(clinic_id)
        create_user(email, password, name, clinic, [specialty] if specialty else [])

    print("ok!")
except ExplainableException as e:
    print(e.explain())
