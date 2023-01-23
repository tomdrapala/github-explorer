import json

import aiohttp
import asyncio
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


async def annotate_commit_count(username, results):
    urls_queue = asyncio.Queue()
    for i, obj in enumerate(results):
        repository = obj['name']
        url = COMMITS_URL.format(username=username, repository=repository)
        await urls_queue.put({'idx': i, 'url': url})

    await asyncio.gather(
        asyncio.create_task(get_commit_count('1', urls_queue, results)),
        asyncio.create_task(get_commit_count('2', urls_queue, results)),
        asyncio.create_task(get_commit_count('3', urls_queue, results)),
        asyncio.create_task(get_commit_count('4', urls_queue, results)),
        asyncio.create_task(get_commit_count('5', urls_queue, results)),
    )
    return results
