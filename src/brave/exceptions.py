from __future__ import annotations

from typing import Any
from typing import Optional
from typing import cast

import httpx


class BraveError(Exception):
    """Base exception class for all Brave Search API errors."""

    pass


class APIError(BraveError):
    """Exception raised when the API returns an error response."""

    message: str
    request: httpx.Request

    body: object | None

    """The API response body.

    If the API responded with a valid JSON structure then this property will be the
    decoded result.

    If it isn't a valid JSON structure then this will be the raw response.

    If there was no response associated with this error then it will be `None`.
    """

    code: Optional[str]
    param: Optional[str]
    type: Optional[str]

    def __init__(self, message: str, request: httpx.Request, *, body: object | None) -> None:
        super().__init__(message)
        self.request = request
        self.message = message

        if isinstance(body, dict):
            self.code = cast(Any, body.get("code"))
            self.param = cast(Any, body.get("param"))
            self.type = cast(Any, body.get("type"))
        else:
            self.code = None
            self.param = None
            self.type = None
