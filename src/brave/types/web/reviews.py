from typing import List

from pydantic import BaseModel
from pydantic import Field

from ..shared.thumbnail import Thumbnail
from .person import Person
from .rating import Rating


class TripAdvisorReview(BaseModel):
    """A model representing a TripAdvisor review."""

    title: str = Field(description="The title of the review.")
    description: str = Field(description="A description seen in the review.")
    date: str = Field(description="The date when the review was published.")
    rating: Rating = Field(description="A rating given by the reviewer.")
    author: Person = Field(description="The author name of the review.")
    review_url: str = Field(description="A URL link to the page where the review can be found.")
    language: str = Field(description="The language of the review.")


class Reviews(BaseModel):
    """The reviews associated with an entity."""

    results: List[TripAdvisorReview] = Field(description="A list of TripAdvisor reviews for the entity.")
    viewMoreUrl: str = Field(description="A URL to a web page where more information on the result can be seen.")
    reviews_in_foreign_language: bool = Field(description="Any reviews available in a foreign language.")


class Review(BaseModel):
    """A model representing a review for an entity."""

    type: str = Field(default="review", description="A string representing review type. This is always review.")
    name: str = Field(description="The review title for the review.")
    thumbnail: Thumbnail = Field(description="The thumbnail associated with the reviewer.")
    description: str = Field(description="A description of the review.")
    rating: Rating = Field(description="The ratings associated with the review.")
