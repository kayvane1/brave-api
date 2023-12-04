from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl

from .profile import Profile


class Result(BaseModel):
    """
    Model represents a web search result.

    url: https://api.search.brave.com/app/documentation/web-search/responses#Result
    """

    title: str = Field(description="The title of the web page.")
    url: HttpUrl = Field(description="The URL where the page is served.")
    is_source_local: Optional[bool] = Field(
        default=None, description="Indicates if the source of the web page is local."
    )
    is_source_both: Optional[bool] = Field(
        default=None, description="Indicates if the source of the web page is both local and non-local."
    )
    description: str = Field(description="A description for the web page.")
    page_age: Optional[str] = Field(default=None, description="A date representing the age of the web page.")
    page_fetched: Optional[str] = Field(
        default=None, description="A date representing when the web page was last fetched."
    )
    language: Optional[str] = Field(default=None, description="A language classification for the web page.")
    profile: Optional[Profile] = Field(default=None, description="A profile associated with the web page.")
    family_friendly: Optional[bool] = Field(default=None, description="Whether the web page is family friendly.")
