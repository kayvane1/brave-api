import json

from brave.types import WebSearchApiResponse


def _load_response():
    with open("tests/test_responses/blue_tack_minimal.json", "r") as f:
        data = json.load(f)
    return WebSearchApiResponse.model_validate(data)


def test_product_cluster_empty():
    response = _load_response()
    assert response.product_cluster == []


def test_product_prices_empty():
    response = _load_response()
    assert response.product_prices() == []


def test_product_price_ranges_empty():
    response = _load_response()
    assert response.product_price_ranges() == (0, 0)


def test_average_product_review_score_none():
    response = _load_response()
    assert response.average_product_review_score() is None
