from typing import List

from pydantic import BaseModel
from pydantic import Field


class DayOpeningHours(BaseModel):
    """A model representing a day opening hour for a business at a particular location."""

    abbr_name: str = Field(description="A short string representing the day of the week.")
    full_name: str = Field(description="A full string representing the day of the week.")
    opens: str = Field(
        description="A 24 hr clock time string for the opening time of the business at the particular day."
    )
    closes: str = Field(
        description="A 24 hr clock time string for the closing time of the business at the particular day."
    )


class OpeningHours(BaseModel):
    """Opening hours of a business at a particular location."""

    current_day: List[DayOpeningHours] = Field(
        description="The current day opening hours. Can have two sets of opening hours."
    )
    days: List[List[DayOpeningHours]] = Field(description="The opening hours for the whole week.")
