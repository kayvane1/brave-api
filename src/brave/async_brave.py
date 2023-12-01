from typing import Dict
from typing import Optional

import httpx

from tenacity import AsyncRetrying
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from brave.client import BraveAPIClient
from brave.exceptions import BraveError
from brave.types import WebSearchApiResponse


class AsyncBrave(BraveAPIClient):
    """Asynchronous client for interacting with the Brave Search API."""

    def __init__(self, api_key: Optional[str] = None, endpoint: str = "web") -> None:
        super().__init__(api_key=api_key, endpoint=endpoint)

    async def _get(self, params: Dict = None) -> httpx.Response:
        """
        Perform an asynchronous GET request to the specified endpoint with optional parameters.

        Includes retry logic using tenacity.
        """
        url = self.base_url + self.endpoint + "/search"
        headers = self._prepare_headers()

        async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_fixed(2)):
            with attempt:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers, params=params)
                    response.raise_for_status()  # Raises HTTPError for bad requests
                    return response

    async def search(
        self,
        q: str,
        country: Optional[str] = None,
        search_lang: Optional[str] = None,
        ui_lang: Optional[str] = None,
        count: Optional[int] = 20,
        offset: Optional[int] = 0,
        safesearch: Optional[str] = "moderate",
        freshness: Optional[str] = None,
        text_decorations: Optional[bool] = True,
        spellcheck: Optional[bool] = True,
        result_filter: Optional[str] = None,
        goggles_id: Optional[str] = None,
        units: Optional[str] = None,
        extra_snippets: Optional[bool] = False,
    ) -> WebSearchApiResponse:
        """
        Perform a search using the Brave Search API.

        Parameters:
        -----------
        q: str
            The search query (required).
        country: str
            The 2-character country code (default: 'US').
        search_lang: str
            The search language preference.
        ui_lang: str
            User interface language preference (default: 'en_US').
        count: int
            The number of results to return (default: 20, max: 20).
        offset: int
            Offset for pagination (default: 0, max: 9).
        safesearch: str
            Filter for adult content ('off', 'moderate', 'strict').
        freshness: str
            Filters results by discovery time.
        text_decorations: bool
            Include decoration markers in display strings (default: True).
        spellcheck: bool
            Spellcheck the query (default: True).
        result_filter: str
            Types of results to include.
        goggles_id: str
            The goggle URL to rerank search results.
        units: str
            Measurement units (metric or imperial).
        extra_snippets: bool
            Enable extra alternate snippets (default: False).
        """

        # Parameter validation and query parameter construction
        if not q or len(q) > 400 or len(q.split()) > 50:
            raise ValueError("Invalid query parameter 'q'")

        params = {
            "q": q,
            "country": country,
            "search_lang": search_lang,
            "ui_lang": ui_lang,
            "count": min(count, 20),
            "offset": min(offset, 9),
            "safesearch": safesearch,
            "freshness": freshness,
            "text_decorations": text_decorations,
            "spellcheck": spellcheck,
            "result_filter": result_filter,
            "goggles_id": goggles_id,
            "units": units,
            "extra_snippets": extra_snippets,
        }

        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}

        # API request and response handling
        response = await self._get(params=params)  # _make_request to be implemented based on sync/async client

        # Error handling and data parsing
        if response.status_code != 200:
            # Handle errors (e.g., log them, raise exceptions)
            raise BraveError(f"API Error: {response.status_code} - {response.text}")

        # return response.json()
        return WebSearchApiResponse.model_validate(response.json())
