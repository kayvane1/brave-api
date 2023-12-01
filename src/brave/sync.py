import logging

from typing import Dict
from typing import Optional

import requests

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from brave.client import BraveAPIClient


logger = logging.getLogger(__name__)


class Brave(BraveAPIClient):
    """Synchronous client for interacting with the Brave Search API."""

    def __init__(self, api_key: Optional[str] = None, endpoint: str = "web") -> None:
        super().__init__(api_key=api_key, endpoint=endpoint)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _get(self, params: Dict = None) -> requests.Response:
        """
        Perform a synchronous GET request to the specified endpoint with optional parameters.

        Includes retry logic using tenacity.
        """
        url = self.base_url + self.endpoint + "/search"
        headers = self._prepare_headers()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises HTTPError for bad requests
            return response
        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request error occurred: {e}")
