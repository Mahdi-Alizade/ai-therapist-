import pytest
from app.services.safety import evaluate_crisis_risk, EMERGENCY_RESPONSE


def test_safety_triggers_on_crisis_english():
    sample_queries = [
        "I feel like I want to die today",
        "I am thinking of suicide",
        "How to hurt myself without pain?",
        "I can't take this anymore, want to end my life",
    ]
    for text in sample_queries:
        result = evaluate_crisis_risk(text)
        assert result is not None
        assert result == EMERGENCY_RESPONSE


def test_safety_triggers_on_crisis_persian():
    sample_queries = [
        "دیگه خسته شدم، می‌خوام بمیرم",
        "فکر خودکشی تو سرمه",
        "می‌خوام به خودم آسیب بزنم",
    ]
    for text in sample_queries:
        result = evaluate_crisis_risk(text)
        assert result is not None
        assert result == EMERGENCY_RESPONSE


def test_safety_allows_normal_conversations():
    safe_queries = [
        "I had a really tiring day at work.",
        "Can we talk about feeling anxious before an interview?",
        "امروز استرس زیادی سر کار داشتم، چطور آروم بشم؟",
        "چرا همیشه احساس تنهایی می‌کنم؟",
    ]
    for text in safe_queries:
        result = evaluate_crisis_risk(text)
        assert result is None