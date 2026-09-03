import re
from typing import Optional

CRISIS_PATTERNS = [
    r"\b(suicide|kill myself|want to die|end my life|self-harm|hurt myself)\b",
    r"(خودکشی|خودزنی|بمیرم|آسیب\s*(?:به\s*خود|به\s*خودم|بزنم|برسانم)|تمومش\s*کنم|تیغ\s*زدن)",
]

EMERGENCY_RESPONSE = (
    "It sounds like you are going through a difficult time. "
    "Please know that you are not alone and support is available:\n\n"
    "- If you are in immediate danger, please call your local emergency services (e.g., 911 in the US, 112 in Europe, 123 in Iran).\n"
    "- In the US and Canada, call or text 988 to reach the Suicide & Crisis Lifeline.\n"
    "- In the UK, call 111.\n\n"
    "This application is an AI experiment and cannot provide medical or crisis care."
)


def evaluate_crisis_risk(user_message: str) -> Optional[str]:
    """
    Evaluates input text for explicit crisis indicators.
    Normalizes spaces and Persian half-spaces (ZWNJ) before regex evaluation.
    Returns standard emergency instructions if triggered, otherwise None.
    """
    if not user_message:
        return None

    # Replace Persian half-space (ZWNJ) and normalize spaces
    normalized_text = user_message.replace("\u200c", " ").lower()

    for pattern in CRISIS_PATTERNS:
        if re.search(pattern, normalized_text, flags=re.IGNORECASE):
            return EMERGENCY_RESPONSE
    return None