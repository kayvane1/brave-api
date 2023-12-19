import json

from unittest.mock import AsyncMock

import httpx
import pytest
import tenacity

from brave.async_brave import AsyncBrave
from brave.types import WebSearchApiResponse


@pytest.mark.asyncio
async def test_async_brave_initialization():
    client = AsyncBrave(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.endpoint == "web"  # Assuming "web" is the default endpoint


@pytest.mark.asyncio
async def test_async_get_success(monkeypatch):
    async def mock_get(*args, **kwargs):
        # Create a Mock Response
        mock_response = httpx.Response(200, json={"data": "test response"})
        # Setting the request attribute
        mock_response._request = httpx.Request(method="GET", url=args[0])
        return mock_response

    monkeypatch.setattr(httpx.AsyncClient, "get", AsyncMock(side_effect=mock_get))

    client = AsyncBrave(api_key="test_key")
    response = await client._get(params={"q": "test query"})
    assert response.json() == {"data": "test response"}


@pytest.mark.asyncio
async def test_async_get_with_retries(monkeypatch):
    call_count = 0

    async def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise httpx.HTTPError("Temporary failure")
        # Create a Mock Response
        mock_response = httpx.Response(200, json={"data": "test response after retries"})
        # Setting the request attribute
        mock_response._request = httpx.Request(method="GET", url=args[0])
        return mock_response

    monkeypatch.setattr(httpx.AsyncClient, "get", AsyncMock(side_effect=mock_get))

    client = AsyncBrave(api_key="test_key")
    response = await client._get(params={"q": "test query"})
    assert call_count == 3
    assert response.json() == {"data": "test response after retries"}


@pytest.mark.asyncio
async def test_async_get_failure(monkeypatch):
    # Mocking httpx.AsyncClient.get to always raise an HTTPError
    monkeypatch.setattr(httpx.AsyncClient, "get", AsyncMock(side_effect=httpx.HTTPError("Permanent failure")))

    client = AsyncBrave(api_key="test_key")

    # Expecting tenacity.RetryError instead of httpx.HTTPError
    with pytest.raises(tenacity.RetryError):
        await client._get(params={"q": "test query"})


@pytest.mark.asyncio
async def test_response_validation(monkeypatch):

    with open("tests/test_responses/blue_tack_minimal.json", "r") as f:
        _mock_response = json.load(f)

    async def mock_get(*args, **kwargs):
        mock_response = httpx.Response(200, json=_mock_response)
        mock_response._request = httpx.Request(method="GET", url=args[0])
        return mock_response

    monkeypatch.setattr(httpx.AsyncClient, "get", AsyncMock(side_effect=mock_get))

    client = AsyncBrave(api_key="test_key")
    response = await client.search("Blue tack")  # Replace with the actual async method
    assert isinstance(response, WebSearchApiResponse)
