import requests


def call_api_project_details(project_id):
    url = f"https://techport.nasa.gov/api/projects/{project_id}"
    headers = {"accept" : "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error while fetching project {project_id}: {e}")
        return None

    project = data.get("project", {})

    result = {
        "title": project.get("title"),
        "destinationType": project.get("destinationType", []),
    }
    return result