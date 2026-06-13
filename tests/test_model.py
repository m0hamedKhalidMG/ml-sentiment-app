"""Tests for sentiment model."""

from src.model import predict_sentiment


def test_positive_sentiment() -> None:
    result = predict_sentiment("This is a wonderful and amazing product!")
    assert result["label"] == "positive"
    assert result["confidence"] >= 0.0


def test_negative_sentiment() -> None:
    result = predict_sentiment("This is terrible and awful.")
    assert result["label"] == "negative"
    assert result["confidence"] >= 0.0


def test_neutral_sentiment() -> None:
    result = predict_sentiment("The sky is blue.")
    assert result["label"] in ("positive", "negative", "neutral")


def test_result_structure() -> None:
    result = predict_sentiment("Hello world")
    assert "label" in result
    assert "confidence" in result
    assert isinstance(result["confidence"], float)


def test_empty_string() -> None:
    result = predict_sentiment("")
    assert "label" in result
    assert "confidence" in result


def test_very_long_text() -> None:
    text = "great " * 1000
    result = predict_sentiment(text)
    assert result["label"] == "positive"
    assert result["confidence"] >= 0.0
