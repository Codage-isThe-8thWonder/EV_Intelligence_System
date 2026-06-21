import requests

from utils.baseURL_config import BASE_URL


def upload_csv(
    vehicle_id: int,
    file,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = {
        "file": (
            file.name,
            file,
            "text/csv"
        )
    }

    response = requests.post(
        f"{BASE_URL}/ev-data/upload/{vehicle_id}",
        headers=headers,
        files=files
    )

    return response