from unittest.mock import Mock
from unittest.mock import patch

from brave.sync import Brave


def test_brave_initialization():
    client = Brave(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.endpoint == "web"  # Assuming "web" is the default endpoint


def test_sync_get_success():
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: {"data": "test response"})

        client = Brave(api_key="test_key")
        response = client._get(params={"q": "test query"})
        assert response.json() == {"data": "test response"}
