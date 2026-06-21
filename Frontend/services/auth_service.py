import requests

from utils.baseURL_config import BASE_URL


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