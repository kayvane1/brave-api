import logging

from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from .not_implemented import FAQ
from .not_implemented import Discussions
from .not_implemented import GraphInfobox
from .not_implemented import Locations
from .not_implemented import MixedResponse
from .not_implemented import News
from .not_implemented import Videos
from .query import Query
from .search import Search
from .search_result import SearchResult


logger = logging.getLogger(__name__)


class WebSearchApiResponse(BaseModel):
    """Brave Search API response object"""

    query: Query = Field(description="Search query string and its modifications that are used for search.")
    mixed: MixedResponse = Field(description="Preferred ranked order of search results.")
    type: str = Field(default="search", description="The type of web search API result. The value is always search.")
    web: Search = Field(description="Web search results relevant to the query.")
    discussions: Optional[Discussions] = Field(
        default=None, description="Discussions clusters aggregated from forum posts that are relevant to the query."
    )
    faq: Optional[FAQ] = Field(
        default=None, description="Frequently asked questions that are relevant to the search query."
    )
    infobox: Optional[GraphInfobox] = Field(
        default=None, description="Aggregated information on an entity showable as an infobox."
    )
    locations: Optional[Locations] = Field(
        default=None, description="Places of interest (POIs) relevant to location sensitive queries."
    )
    news: Optional[News] = Field(default=None, description="News results relevant to the query.")
    videos: Optional[Videos] = Field(default=None, description="Videos relevant to the query.")

    def __str__(self) -> str:
        """Return the model as a JSON string."""
        return self.model_dump_json(indent=4)

    @property
    def results(self) -> List[SearchResult]:
        """Property to access the list of search results directly."""
        return self.web.results if self.web and self.web.results else []

    def download_all_pdfs(self, path: str = "downloads") -> None:
        """Download PDFs for all search results."""
        for result in self.results:
            if result.content_type == "pdf":
                result.download_pdf(path=path)
