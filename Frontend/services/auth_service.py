import requests

BASE_URL = "http://127.0.0.1:8000"


def register_user(payload):

    response = requests.post(
        f"{BASE_URL}/users/register",
        json=payload
    )

    return response


def login_user(payload):

    response = requests.post(
        f"{BASE_URL}/users/login",
        json=payload
    )

    return response