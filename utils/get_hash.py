from werkzeug.security import generate_password_hash

print(generate_password_hash(input("Input password: ")))