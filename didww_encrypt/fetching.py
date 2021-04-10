from urllib.request import urlopen
import json


def fetch_public_keys(uri: str) -> (str, str):
    response = urlopen(uri)
    payload = json.loads(response.read())
    return (
        payload["data"][0]["attributes"]["key"],
        payload["data"][1]["attributes"]["key"],
    )
