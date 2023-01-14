from typing import Union

from pydantic import BaseModel, HttpUrl


class Repository(BaseModel):
    """Repository data model"""
    name: str
    description: Union[str, None] = None
    url: Union[HttpUrl, None] = None
    stars: Union[int, None] = None
    commits: Union[int, None] = None
    # Using Union to make sure that code will work on older Python versions
