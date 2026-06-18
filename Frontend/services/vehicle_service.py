import requests

BASE_URL = "http://127.0.0.1:8000"


def add_vehicle(payload, token):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{BASE_URL}/vehicles/add",
        json=payload,
        headers=headers
    )

    return response


def get_all_vehicles(token):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/vehicles/get_all",
        headers=headers
    )

    return response


def get_vehicle_by_id(
    vehicle_id,
    token
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/vehicles/get/{vehicle_id}",
        headers=headers
    )

    return response


def delete_vehicle(
    vehicle_id: int,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.delete(
        f"{BASE_URL}/vehicles/remove/{vehicle_id}",
        headers=headers
    )

    return response