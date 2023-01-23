import asyncio
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware

from .models import Repository
from .utils import COMMITS_URL, get_commit_count, get_repository_data

app = FastAPI(title="GitHub Explorer API")

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


USERNAME_MAX_LENGTH = 39  # maximum username length allowed by GitHub


# In real project I would move below endpoint to a dedicated file,
# I am leaving it here for simplicity.

@app.get('/{username}/', tags=["GitHub"], response_model=List[Repository])
async def get_user_repositories(username: str = Path(max_length=USERNAME_MAX_LENGTH)):
    """Retrieve basic information about GitHub repositories belonging to the given user."""
    data = get_repository_data(username)
    if data['status_code'] == status.HTTP_200_OK:
        results = list()
        for obj in data['content']:
            results.append({
                "url": obj.get("html_url"),
                "name": obj.get("name"),
                "description": obj.get("description"),
                "stars": obj.get("stargazers_count")
            })

        # Get commit count for each repository by making series of asynchornious requests
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

    elif (
        data['status_code'] == status.HTTP_403_FORBIDDEN and
        data['rate_limit']['remaining'] == 0
    ):
        # If the API rate limit has been reached return information about when will it be reset.
        message = 'API rate limit exceeded, please try again'
        if data['rate_limit']['reset_time'] != 0:
            reset_time = datetime.fromtimestamp(data['rate_limit']['reset_time'])
            wait_time = (reset_time - datetime.now()).seconds // 60
            message = message + f" in {wait_time} minutes."
        else:
            message = message + " later."
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": message}
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "User not found, please try a different username."}
    )
