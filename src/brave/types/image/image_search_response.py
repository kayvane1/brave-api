from typing import List

from pydantic import BaseModel
from pydantic import Field

from .image_query import Query
from .image_result import ImageResult


class ImageSearchApiResponse(BaseModel):
    """Top level response model for successful Image Search API requests."""

    type: str = Field(default="images", description="The type of search API result. The value is always images.")
    query: Query = Field(description="Image search query string.")
    results: List[ImageResult] = Field(description="The list of image results for the given query.")
