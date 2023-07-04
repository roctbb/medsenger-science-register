from backend.methods import *
from backend.server import app

try:

    with app.app_context():
        create_patient("Иванов Иван", Sex.MALE, datetime.now())

    print("ok!")
except ExplainableException as e:
    print(e.explain())
