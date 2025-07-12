import requests


def http_get(endpoint: str, params: dict) -> requests.Response:
    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    return response