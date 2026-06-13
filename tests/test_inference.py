"""Tests for the FastAPI inference server."""

from fastapi.testclient import TestClient

from src.inference import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_positive() -> None:
    response = client.post("/predict", json={"text": "I love this product!"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] in ("positive", "negative", "neutral")
    assert "confidence" in data


def test_predict_empty_text() -> None:
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 400


def test_predict_missing_field() -> None:
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_negative() -> None:
    response = client.post("/predict", json={"text": "I hate this product!"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "negative"
    assert "confidence" in data


def test_predict_whitespace_only() -> None:
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 400
