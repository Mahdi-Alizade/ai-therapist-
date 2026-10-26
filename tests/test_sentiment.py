import pytest
from app.services.sentiment import analyze_text_sentiment


def test_sentiment_identifies_distress_and_stress_score():
    distressed_input = "I am so overwhelmed and exhausted with this burnout."
    result = analyze_text_sentiment(distressed_input)

    assert result["valence"] == "distressed"
    assert result["stress_score"] > 0.0
    assert "burnout" in result["detected_cues"] or "overwhelmed" in result["detected_cues"]


def test_sentiment_identifies_positive_relief():
    calm_input = "I feel much more calm and clear right now."
    result = analyze_text_sentiment(calm_input)

    assert result["valence"] == "positive"
    assert "calm" in result["detected_cues"]


def test_sentiment_identifies_persian_markers():
    persian_input = "خیلی احساس خستگی و اضطراب می‌کنم و همه‌چیز غیرممکنه."
    result = analyze_text_sentiment(persian_input)

    assert result["valence"] == "distressed"
    assert result["cognitive_rigidity"] is True


def test_empty_input_returns_safe_defaults():
    empty_result = analyze_text_sentiment("")
    assert empty_result["stress_score"] == 0.0
    assert empty_result["valence"] == "neutral"