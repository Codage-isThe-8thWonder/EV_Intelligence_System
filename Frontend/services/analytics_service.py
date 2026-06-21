import requests
from utils.baseURL_config import BASE_URL

# BASE_URL = "http://backend:8000"    ----   For docker-Compose running changed the URL


def get_summary_card(
    vehicle_id: int,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/analytics/summary_card/{vehicle_id}",
        headers=headers
    )

    return response


def get_operational_trends(
    vehicle_id: int,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/analytics/trends/{vehicle_id}",
        headers=headers
    )

    return response


def get_battery_analytics(
    vehicle_id: int,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/analytics/battery-analytics/{vehicle_id}",
        headers=headers
    )

    return response


def get_vehicle_performance(
    vehicle_id: int,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{BASE_URL}/analytics/vehicle-performance/{vehicle_id}",
        headers=headers
    )

    return response