import requests
from pprint import pprint
from db import upsert_project


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

    print("Creating Database - this may take a few minutes.")

    for project in data["projects"]:
        upsert_project(project)

    print("Done!")

    return



'''
curl -X 'GET' \
  'https://techport.nasa.gov/api/projects/118419' \
  -H 'accept: application/json'


    "title": "Scalable Hybrid Manufacturing of Bimetallic Components for Space Applications",

    "description": "<p> \tThe Space Technology Research Grants Program will accelerate the development of &quot;push&quot; technologies to support the future space science and exploration needs of NASA, other government agencies and the commercial space sector. Innovative efforts with high risk and high payoff will be encouraged. The program is composed of two competitively awarded components.</p> ",

    "destinationType": [
        "Earth"
        ],
'''