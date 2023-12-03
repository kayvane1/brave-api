from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from .profile import Profile


class Rating(BaseModel):
    """The rating associated with an entity."""

    ratingValue: Optional[float] = Field(default=None, description="The current value of the rating.")
    bestRating: Optional[float] = Field(default=None, description="Best rating received.")
    reviewCount: Optional[int] = Field(default=None, description="The number of reviews for the rating.")
    profile: Optional[Profile] = Field(default=None, description="The profile associated with the rating.")
    is_tripadvisor: Optional[bool] = Field(default=False, description="Is the rating coming from TripAdvisor.")
