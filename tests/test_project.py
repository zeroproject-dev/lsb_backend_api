import requests

BASE_PATH = "http://127.0.0.1:3300"


def test_home():
    r = requests.get(f"{BASE_PATH}/")
    assert r.status_code == 200


def test_users():
    r = requests.get(f"{BASE_PATH}/api/v1/users/")
    assert r.status_code == 200


def test_users_res():
    r = requests.get(f"{BASE_PATH}/api/v1/users/")
    assert "admin@gmail.com" in r.text


def test_users_create():
    data = {
        "first_name": "Jesus",
        "second_name": "Andres",
        "first_surname": "Copeticona",
        "second_surname": "Justiniano",
        "email": "andrescopeticona7@gmail.com",
        "role": 2,
    }

    r = requests.post(f"{BASE_PATH}/api/v1/users/", json=data)
    assert r.status_code == 200


def test_users_get_by_id():
    r = requests.get(f"{BASE_PATH}/api/v1/users/1")
    assert (
        r.text.replace("\n", "").replace(" ", "")
        == '{ "email": "admin@gmail.com", "first_name": "Admin", "first_surname": "Admin", "id": 1, "password": "sha256$DqBixignPwmuuduT$77efdc09a8f62a3339ce905c5358334bd9a11f8313d256a6872f0ca91500515e", "role": 1, "second_name": "Admin", "second_surname": "Admin", "state": "active" }'.replace(
            " ", ""
        )
    )


def test_users_update():
    data = {
        "first_name": "Pepito",
        "second_name": "Juan",
        "first_surname": "Copeticona",
        "second_surname": "Justiniano",
        "email": "andrescopeticona7@gmail.com",
        "role": 1,
    }

    r = requests.put(f"{BASE_PATH}/api/v1/users/2", json=data)
    assert r.status_code == 200
