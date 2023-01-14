import json
from datetime import datetime

import requests
from fastapi import status

BASE_URL = "https://api.github.com/"
USER_URL = BASE_URL + "users/{username}/repos"
COMMITS_URL = BASE_URL + "repos/{username}/{repository}/commits"


def get_repository_data(username):
    url = USER_URL.format(username=username)
    response = requests.get(url)
    return {
        "status_code": response.status_code,
        "content": json.loads(response.content)
    }


def get_commits_count(username, repository):
    response = requests.get(COMMITS_URL.format(username=username, repository=repository))
    if response.status_code == status.HTTP_200_OK:
        data = json.loads(response.content)
        return len(data)


def get_rate_reset_time():
    response = requests.get('https://api.github.com/rate_limit')
    response = json.loads(response.content)
    reset = response.get('resources', {}).get('core', {}).get('reset')
    if reset and isinstance(reset, int):
        return datetime.fromtimestamp(reset)
