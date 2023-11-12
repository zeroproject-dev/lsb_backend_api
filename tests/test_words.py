import requests

BASE_PATH = "http://127.0.0.1:3300"


def test_words():
    r = requests.get(f"{BASE_PATH}/api/v1/words/")
    assert r.status_code == 200


def test_words_create():
    data = {"word": "te amo"}

    r = requests.post(f"{BASE_PATH}/api/v1/words/", json=data)
    assert r.status_code == 200


def test_words_get_by_id():
    r = requests.get(f"{BASE_PATH}/api/v1/words/1")
    assert "te amo" in r.text


def test_words_update():
    data = {"word": "hola"}

    r = requests.put(f"{BASE_PATH}/api/v1/words/1", json=data)
    assert r.status_code == 200
