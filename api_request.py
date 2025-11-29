import requests
from pprint import pprint


def call_api(date):
    url = "https://techport.nasa.gov/api/projects"
    params = {
        "updatedSince": f"{date}"
    }
    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)

    response.raise_for_status()

    data = response.json()

    pprint(data)