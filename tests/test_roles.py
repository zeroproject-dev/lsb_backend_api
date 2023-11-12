import requests

BASE_PATH = "http://127.0.0.1:3300"


def test_roles():
    r = requests.get(f"{BASE_PATH}/api/v1/roles/")
    assert r.status_code == 200


def test_roles_create():
    data = {
        "name": "prueba",
        "description": "esto es una prueba",
        "state": True,
        "usuarios": [True, True, False, False],
        "roles": [True, True, False, False],
        "words": [True, True, False, False],
    }

    r = requests.post(f"{BASE_PATH}/api/v1/roles/", json=data)
    assert r.status_code == 200


def test_roles_get_by_id():
    r = requests.get(f"{BASE_PATH}/api/v1/roles/3")
    assert "esto es una prueba" in r.text
