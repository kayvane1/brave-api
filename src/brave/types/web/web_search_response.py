import logging

from typing import List
from typing import Optional
from typing import Tuple

import numpy as np

from pydantic import BaseModel
from pydantic import Field

from .discussions import Discussions
from .faq import FAQ
from .info_box import GraphInfobox
from .location_result import Locations
from .mixed_response import MixedResponse
from .news import News
from .query import Query
from .search import Search
from .search_result import SearchResult
from .videos import Videos


logger = logging.getLogger(__name__)


class WebSearchApiResponse(BaseModel):
    """Brave Search API response object"""

    query: Query = Field(description="Search query string and its modifications that are used for search.")
    mixed: Optional[MixedResponse] = Field(default=None, description="Preferred ranked order of search results.")
    type: str = Field(default="search", description="The type of web search API result. The value is always search.")
    web: Optional[Search] = Field(default=None, description="Web search results relevant to the query.")
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
        return self.model_dump_json(indent=4, exclude_unset=True)

    @property
    def web_results(self) -> List[SearchResult]:
        """Property to access the list of search results directly."""
        _results = self.model_dump(exclude_defaults=True, exclude_unset=True)
        return _results.get("web").get("results") if self.web and self.web.results else []

    @property
    def _web_results(self) -> List[SearchResult]:
        """Property to access the list of search results directly."""
        return self.web.results if self.web and self.web.results else []

    @property
    def urls(self) -> List[str]:
        """Return a list of URLs."""
        return [result.url for result in self._web_results if result.url]

    @property
    def review_urls(self) -> List[str]:
        """Return a list of review URLs."""
        return [result.url for result in self._web_results if result.subtype == "product" and result.review]

    @property
    def descriptions(self) -> List[str]:
        """Return a list of descriptions."""
        return [result.description for result in self._web_results if result.description]

    @property
    def news_results(self) -> List[str]:
        """Return a list of news articles."""
        _results = self.model_dump(exclude_defaults=True, exclude_unset=True)
        return _results.get("news").get("results") if self.news else []

    @property
    def video_results(self) -> List[str]:
        """Return a list of video links."""
        _results = self.model_dump(exclude_defaults=True, exclude_unset=True)
        return _results.get("videos").get("results") if self.videos else []

    @property
    def product_cluster(self) -> List[str]:
        """Return a list of product clusters."""
        return [result.product_cluster for result in self._web_results if result.subtype == "product_cluster"][0]

    def download_all_pdfs(self, path: str = "downloads") -> None:
        """Download PDFs for all search results."""
        for result in self._web_results:
            if result.content_type == "pdf":
                result.download_pdf(path=path)

    def product_prices(self) -> List[int]:
        """Return a list of product prices."""
        if len(self.product_cluster) == 0:
            return [
                float(result.product.price) for result in self._web_results if result.product and result.product.price
            ]
        else:
            return [float(result.price) for result in self.product_cluster]

    def product_price_ranges(self) -> Tuple[int, int]:
        """Return a list of product price ranges."""
        prices = self.product_prices()
        return (min(prices), max(prices))

    def average_product_review_score(self) -> Optional[float]:
        """Return the average product review score out of 100."""
        if len(self.product_cluster) == 0:
            ratings = [
                float(result.product.rating.ratingValue) / float(result.product.rating.bestRating)
                for result in self._web_results
                if result.product and result.product.rating
            ]
        else:
            ratings = [
                float(product.rating.ratingValue) / float(product.rating.bestRating)
                for product in self.product_cluster
                if product.rating and product.rating.ratingValue and product.rating.bestRating
            ]
        if ratings:
            return np.mean([r for r in ratings if r is not None]) * 100
        else:
            return None
