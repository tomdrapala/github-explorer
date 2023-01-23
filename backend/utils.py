import json

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
        "content": json.loads(response.content),
        "rate_limit": {
            "remaining": int(response.headers.get('X-RateLimit-Remaining') or 0),
            "reset_time": int(response.headers.get('X-RateLimit-Reset') or 0)
        }
    }


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
