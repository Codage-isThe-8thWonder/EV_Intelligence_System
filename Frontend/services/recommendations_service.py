import requests

from utils.baseURL_config import BASE_URL


def get_recommendations(
    vehicle_id: int,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/recommendations/{vehicle_id}",
        headers=headers
    )

    return response