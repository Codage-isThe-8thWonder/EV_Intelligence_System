import requests

from utils.baseURL_config import BASE_URL


def get_predictions(
    vehicle_id: int,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/predictions/{vehicle_id}",
        headers=headers
    )

    return response