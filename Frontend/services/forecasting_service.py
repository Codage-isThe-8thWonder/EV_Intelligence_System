import requests

BASE_URL = "http://backend:8000"


def get_forecast(
    vehicle_id: int,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/forecasting/{vehicle_id}",
        headers=headers
    )

    return response