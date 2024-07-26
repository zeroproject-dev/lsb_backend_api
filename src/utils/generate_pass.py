from werkzeug.security import generate_password_hash

while True:
    password = input("Enter password: ")

    if len(password) < 2:
        break

    print(generate_password_hash(password))
