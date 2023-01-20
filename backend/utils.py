import json
from datetime import datetime

import aiohttp
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


def get_rate_reset_time():
    response = requests.get('https://api.github.com/rate_limit')
    response = json.loads(response.content)
    reset = response.get('resources', {}).get('core', {}).get('reset')
    if reset and isinstance(reset, int):
        return datetime.fromtimestamp(reset)


async def get_commit_count(num, urls_queue, data):
    async with aiohttp.ClientSession() as session:
        while not urls_queue.empty():
            obj = await urls_queue.get()
            async with session.get(obj['url']) as response:
                await response.text()
                if response.status == status.HTTP_200_OK:
                    count = len(json.loads(response._body))
                    data[obj['idx']]['commits'] = count
            print(f"Returning from task {num}")
    return data
