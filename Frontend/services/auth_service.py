import requests

BASE_URL = "http://backend:8000"


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