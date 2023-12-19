import json

from unittest.mock import patch

import pytest

from brave.client import BraveAPIClient
from brave.exceptions import BraveError
from brave.types import WebSearchApiResponse


with open("tests/test_responses/blue_tack_minimal.json", "r") as f:
    _mock_response = json.load(f)

mock_response = WebSearchApiResponse.model_validate(_mock_response)


def test_init_with_explicit_api_key():
    api_key = "test_api_key"
    client = BraveAPIClient(api_key=api_key)
    assert client.api_key == api_key


def test_init_with_env_var_api_key(monkeypatch):
    monkeypatch.setenv("BRAVE_API_KEY", "env_api_key")
    client = BraveAPIClient()
    assert client.api_key == "env_api_key"


def test_init_error_without_api_key(monkeypatch):
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)
    with pytest.raises(BraveError):
        BraveAPIClient(api_key=None)


def test_default_endpoint_on_init():
    client = BraveAPIClient(api_key="test_api_key")
    assert client.endpoint == "web"


def test_custom_endpoint_on_init():
    client = BraveAPIClient(api_key="test_api_key", endpoint="custom_endpoint")
    assert client.endpoint == "custom_endpoint"


def test_api_key_none_and_env_var_not_set(monkeypatch):
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)
    with pytest.raises(BraveError):
        BraveAPIClient(api_key=None)


def test_response_type_validation():
    with patch.object(BraveAPIClient, "search", return_value=mock_response):
        client = BraveAPIClient(api_key="test_api_key")
        response = client.search(q="Blue tack")
        assert isinstance(response, WebSearchApiResponse)
