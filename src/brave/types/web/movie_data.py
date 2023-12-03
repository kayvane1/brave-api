from typing import List

from pydantic import BaseModel
from pydantic import Field

from ..shared.thumbnail import Thumbnail
from .person import Person
from .rating import Rating


class MovieData(BaseModel):
    """Aggregated data for a movie result."""

    name: str = Field(description="Name of the movie.")
    description: str = Field(description="A short plot summary for the movie.")
    url: str = Field(description="A URL serving a movie profile page.")
    thumbnail: Thumbnail = Field(description="A thumbnail for a movie poster.")
    release: str = Field(description="The release date for the movie.")
    directors: List[Person] = Field(description="A list of people responsible for directing the movie.")
    actors: List[Person] = Field(description="A list of actors in the movie.")
    rating: Rating = Field(description="Rating provided to the movie from various sources.")
    duration: str = Field(description="The runtime of the movie. The format is HH:MM:SS.")
    genre: List[str] = Field(description="List of genres in which the movie can be classified.")
    query: str = Field(description="The query that resulted in the movie result.")
