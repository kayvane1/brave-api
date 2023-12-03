from typing import List

from pydantic import BaseModel
from pydantic import Field

from .search_result import SearchResult


class Search(BaseModel):
    """
    Model represents a collection of web search results.

    url: https://api.search.brave.com/app/documentation/web-search/responses#Search
    """

    type: str = Field(
        default="search", description="A type identifying web search results. The value is always search."
    )
    results: List[SearchResult] = Field(description="A list of web search results.")
    family_friendly: bool = Field(description="Whether the web search results are family friendly.")
