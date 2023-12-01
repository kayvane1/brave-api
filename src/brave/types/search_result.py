import logging
import os

from typing import List
from typing import Optional

import requests

from pydantic import Field

from brave.exceptions import BraveError

from .meta_url import MetaUrl
from .not_implemented import FAQ
from .not_implemented import QA
from .not_implemented import Article
from .not_implemented import Book
from .not_implemented import Cluster
from .not_implemented import CreativeWork
from .not_implemented import Location
from .not_implemented import Movie
from .not_implemented import MusicRecording
from .not_implemented import Product
from .not_implemented import Rating
from .not_implemented import Restaurant
from .not_implemented import Review
from .not_implemented import Software
from .not_implemented import Video
from .result import Result
from .thumbnail import Thumbnail


logger = logging.getLogger(__name__)


class SearchResult(Result):
    """
    Aggregated information on a web search result, relevant to the query.

    url: https://api.search.brave.com/app/documentation/web-search/responses#SearchResult
    """

    type: str = Field(
        default="search_result",
        description="A type identifying a web search result. The value is always search_result.",
    )
    subtype: str = Field(default="generic", description="A sub type identifying the web search result type.")
    deep_results: Optional[List] = Field(description="Gathered information on a web search result.")
    schemas: Optional[List] = Field(description="A list of schemas extracted from the web search result.")
    meta_url: MetaUrl = Field(description="Aggregated information on the URL associated with the web search result.")
    thumbnail: Optional[Thumbnail] = Field(description="The thumbnail of the web search result.")
    age: Optional[str] = Field(description="A string representing the age of the web search result.")
    language: str = Field(description="The main language on the web search result.")
    restaurant: Optional[Restaurant] = Field(description="If a location result, associated restaurant information.")
    locations: Optional[List[Location]] = Field(description="The locations associated with the web search result.")
    video: Optional[Video] = Field(description="The video associated with the web search result.")
    movie: Optional[Movie] = Field(description="The movie associated with the web search result.")
    faq: Optional[FAQ] = Field(description="Any frequently asked questions associated with the web search result.")
    qa: Optional[QA] = Field(description="Any question answer information associated with the web search result page.")
    book: Optional[Book] = Field(description="Any book information associated with the web search result page.")
    rating: Optional[Rating] = Field(description="Rating found for the web search result page.")
    article: Optional[Article] = Field(description="An article found for the web search result page.")
    product: Optional[Product] = Field(
        description="The main product and a review that is found on the web search result page."
    )
    product_cluster: Optional[List[Product]] = Field(
        description="A list of products and reviews that are found on the web search result page."
    )
    cluster_type: Optional[str] = Field(description="A type representing a cluster. The value can be product_cluster.")
    cluster: Optional[Cluster] = Field(description="A list of web search results.")
    creative_work: Optional[CreativeWork] = Field(
        description="Aggregated information on the creative work found on the web search result."
    )
    music_recording: Optional[MusicRecording] = Field(
        description="Aggregated information on music recording found on the web search result."
    )
    review: Optional[Review] = Field(
        description="Aggregated information on the review found on the web search result."
    )
    software: Optional[Software] = Field(
        description="Aggregated information on a software product found on the web search result page."
    )
    content_type: Optional[str] = Field(description="The content type associated with the search result page.")
    extra_snippets: Optional[List[str]] = Field(description="A list of extra alternate snippets for the web page.")

    def download_pdf(self, path: str = "downloads") -> None:
        """
        Download a PDF file from the specified URL.

        Parameters:
        -----------
        url : str
            The URL of the PDF file.
        filename : str
            The name of the file to save the PDF to.
        """
        try:
            # check if directory "downloads" exists
            if not os.path.exists(path):
                os.makedirs(path)
            response = requests.get(self.url.__str__())
            if response.status_code == 200:
                with open(f"{path}/{self.title}-{self.age}.pdf", "wb") as f:
                    f.write(response.content)
            else:
                logger.warning("Error: Unable to download the file. Status code:", response.status_code)
        except Exception as e:
            logger.info(BraveError(f"Error downloading PDF: {e}"))
