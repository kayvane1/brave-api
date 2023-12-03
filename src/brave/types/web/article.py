from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from ..shared.thumbnail import Thumbnail
from .person import Person


class Organization(Person):
    """An entity responsible for another entity."""

    type: str = Field(
        default="organization",
        description="A type string identifying an organization. The value is always organization.",
    )


class Article(BaseModel):
    """A model representing an article."""

    author: Optional[List[Person]] = Field(default=None, description="The author of the article.")
    date: Optional[str] = Field(default=None, description="The date when the article was published.")
    publisher: Optional[Organization] = Field(default=None, description="The name of the publisher for the article.")
    thumbnail: Optional[Thumbnail] = Field(default=None, description="A thumbnail associated with the article.")
    isAccessibleForFree: Optional[bool] = Field(
        default=None, description="Whether the article is free to read or is behind a paywall."
    )
