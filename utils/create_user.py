from backend.methods import *
from backend.server import app

try:
    email = input("email:")
    name = input("name:")
    clinic_id = input("clinic_id:")
    specialty = input('specialty:')

    with app.app_context():
        clinic = find_clinic_by_id(clinic_id)

        if not clinic:
            print("Clinic not found")
        else:
            user = create_user(email, name, clinic, [specialty] if specialty else [])
            print("Activation key: ", user.activation_key)
            print("ok!")
except ExplainableException as e:
    print(e.explain())
