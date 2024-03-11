from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from ..shared.meta_url import MetaUrl
from ..shared.thumbnail import Thumbnail
from .result import Result


class NewsResult(Result):
    """A model representing news results."""

    meta_url: Optional[MetaUrl] = Field(
        default=None, description="The aggregated information on the URL representing a news result."
    )
    source: Optional[str] = Field(default=None, description="The source of the news.")
    breaking: Optional[bool] = Field(default=None, description="Whether the news result is currently a breaking news.")
    thumbnail: Optional[Thumbnail] = Field(default=None, description="The thumbnail associated with the news result.")
    age: Optional[str] = Field(default=None, description="A string representing the age of the news article.")
    url: Optional[str] = Field(default=None, description="Url of the news result")
    extra_snippets: Optional[List[str]] = Field(
        default=None, description="A list of extra alternate snippets for the news search result."
    )


class News(BaseModel):
    """A model representing news results."""

    type: str = Field(default="news", description="The type representing the news. The value is always news.")
    results: List[NewsResult] = Field(description="A list of news results.")
    mutated_by_goggles: bool = Field(description="Whether the news result were changed by a goggle.")
