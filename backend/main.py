from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware

from .models import Repository
from .utils import (get_commits_count, get_rate_reset_time, get_repository_data)

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
                "stars": obj.get("stargazers_count"),
                "commits": get_commits_count(username, obj.get("name"))
                # Getting count of commits this way may be slow.
                # As an improvement we could gather all the repositories names
                # and send requests to all of them asynchronously.
            })
        return results

    elif (
        data['status_code'] == status.HTTP_403_FORBIDDEN and
        data['content']['message'].startswith("API rate limit exceeded")
    ):
        # If the API rate limit has been reached return information about when will it be reset.
        message = 'API rate limit exceeded, please try again'
        reset_time = get_rate_reset_time()
        if reset_time:
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
