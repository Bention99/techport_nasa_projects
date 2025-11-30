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
        "startDate": project.get("startDate"),
        "endDate": project.get("endDate"),
        "startYear": project.get("startYear"),
        "endYear": project.get("endYear"),
        "status": project.get("status"),
        "releaseStatus": project.get("releaseStatus"),
        "viewCount": project.get("viewCount"),
        "description": project.get("description"),
    }
    return result