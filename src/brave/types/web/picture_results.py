from typing import List

from pydantic import BaseModel
from pydantic import Field

from ..shared.thumbnail import Thumbnail


class PictureResults(BaseModel):
    """A model representing a list of pictures."""

    viewMoreUrl: str = Field(description="A URL to view more pictures.")
    results: List[Thumbnail] = Field(description="A list of thumbnail results.")
