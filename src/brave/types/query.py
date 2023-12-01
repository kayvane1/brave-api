import logging

from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from .language import Language


logger = logging.getLogger(__name__)


class Query(BaseModel):
    """
    A model representing information gathered around the requested query.

    url: https://api.search.brave.com/app/documentation/web-search/responses#Query
    """

    original: str = Field(description="The original query that was requested.")
    show_strict_warning: bool = Field(
        description="Whether there is more content available for query, but the response was restricted due to safesearch."
    )
    altered: Optional[str] = Field(default=None, description="The altered query for which the search was performed.")
    safe_search: Optional[bool] = Field(default=None, description="Whether safesearch was enabled.")
    is_navigational: bool = Field(description="Whether the query is a navigational query to a domain.")
    is_news_breaking: bool = Field(description="Whether the query has location relevance.")
    local_decision: Optional[str] = Field(
        default=None, description="Whether the query was decided to be location sensitive."
    )
    local_locations_idx: Optional[int] = Field(default=None, description="The index of the location.")
    is_trending: Optional[bool] = Field(default=None, description="Whether the query is trending.")
    ask_for_location: Optional[bool] = Field(
        default=None, description="Whether the query requires location information for better results."
    )
    language: Optional[Language] = Field(default=None, description="The language information gathered from the query.")
    spellcheck_off: bool = Field(description="Whether the spellchecker was off.")
    country: str = Field(description="The country that was used.")
    bad_results: bool = Field(description="Whether there are bad results for the query.")
    should_fallback: bool = Field(description="Whether the query should use a fallback.")
    lat: Optional[str] = Field(default=None, description="The gathered location latitude associated with the query.")
    long: Optional[str] = Field(default=None, description="The gathered location longitude associated with the query.")
    postal_code: Optional[str] = Field(default=None, description="The gathered postal code associated with the query.")
    city: Optional[str] = Field(default=None, description="The gathered city associated with the query.")
    state: Optional[str] = Field(default=None, description="The gathered state associated with the query.")
    header_country: Optional[str] = Field(default=None, description="The country for the request origination.")
    more_results_available: bool = Field(description="Whether more results are available for the given query.")
    custom_location_label: Optional[str] = Field(
        default=None, description="Any custom location labels attached to the query."
    )
    reddit_cluster: Optional[str] = Field(default=None, description="Any Reddit cluster associated with the query.")
