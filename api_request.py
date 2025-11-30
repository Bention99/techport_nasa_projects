import requests
from db import insert_into_db
from log_handling import write_critical_log, write_info_log


def call_api(date):
    url = "https://techport.nasa.gov/api/projects"
    params = {"updatedSince": f"{date}"}
    headers = {"accept": "application/json"}
    api_string = f"{url}, {params}, {headers}"

    try:
        write_info_log(f"Calling API - {api_string}")
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        write_critical_log(f"API Error: {e}")
        print(f"API Error: {e}")
        return None

    insert_into_db(data)
    return

