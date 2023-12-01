import logging
import os

from typing import List
from typing import Optional

import requests

from pydantic import BaseModel
from pydantic import HttpUrl

from brave.exceptions import BraveError


logger = logging.getLogger(__name__)


class Profile(BaseModel):
    """Profile of the website"""

    name: str
    url: HttpUrl
    long_name: str
    img: HttpUrl


class MetaUrl(BaseModel):
    """Metadata of the URL"""

    scheme: str
    netloc: str
    hostname: str
    favicon: HttpUrl
    path: str


class Thumbnail(BaseModel):
    """Thumbnail of the website"""

    src: HttpUrl
    original: HttpUrl
    logo: bool


class SearchResult(BaseModel):
    """Search result object"""

    title: str
    url: HttpUrl
    is_source_local: bool
    is_source_both: bool
    description: str
    page_age: Optional[str] = None
    profile: Profile
    language: str
    family_friendly: bool
    type: str
    subtype: str
    meta_url: MetaUrl
    thumbnail: Optional[Thumbnail] = None
    age: Optional[str] = None
    content_type: Optional[str] = None

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


class Web(BaseModel):
    """Web search results"""

    type: str
    results: List[SearchResult]
    family_friendly: bool


class Query(BaseModel):
    """Query object"""

    original: str
    show_strict_warning: bool
    is_navigational: bool
    is_news_breaking: bool
    spellcheck_off: bool
    country: str
    bad_results: bool
    should_fallback: bool
    postal_code: Optional[str] = None
    city: Optional[str] = None
    header_country: Optional[str] = None
    more_results_available: bool
    state: Optional[str] = None


class BraveSearchResponse(BaseModel):
    """Brave Search API response object"""

    query: Query
    mixed: dict  # Can be more detailed depending on the mixed object's structure
    type: str
    web: Web

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
