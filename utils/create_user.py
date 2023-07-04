from backend.methods import *
from backend import app

try:
    email = input("email:")
    password = input("password:")
    name = input("name:")

    with app.app_context():
        create_user(email, password, name)

    print("ok!")
except ExplainableException as e:
    print(e.explain())
