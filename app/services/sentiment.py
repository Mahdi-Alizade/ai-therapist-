import re
from typing import Dict, List, Any

POSITIVE_MARKERS = {
    "hope", "better", "calm", "relief", "peace", "clear", "grateful",
    "understanding", "progress", "relaxed", "happy", "stable",
    "امید", "بهتر", "آرامش", "راحت", "واضح", "خوب", "پیشرفت", "خوشحال"
}

DISTRESS_MARKERS = {
    "anxious", "panic", "overwhelmed", "stuck", "hopeless", "sad",
    "exhausted", "burnout", "angry", "tired", "fear", "lonely", "confused",
    "اضطراب", "استرس", "وحشت", "درمانده", "غمگین", "خسته", "فرسوده", "عصبانی", "ترس", "تنها"
}

COGNITIVE_RIGIDITY_PATTERNS = [
    r"\b(always|never|must|should|ruined|impossible|failed)\b",
    r"(همیشه|هرگز|باید|حتما|نابود|غیر\s*ممکن(?:ه)?|شکست)"
]


def analyze_text_sentiment(text: str) -> Dict[str, Any]:
    """
    Evaluates emotional valence, stress index, and cognitive rigidity cues
    from the user's conversational text with flexible pattern matching.
    """
    if not text:
        return {
            "stress_score": 0.0,
            "valence": "neutral",
            "detected_cues": [],
            "cognitive_rigidity": False
        }

    # Normalize Persian half-space (ZWNJ) and lower-case
    normalized_text = text.replace("\u200c", " ").lower()
    tokens = re.findall(r"\b\w+\b", normalized_text, flags=re.UNICODE)
    total_words = len(tokens)

    positive_hits: List[str] = []
    distress_hits: List[str] = []
    rigidity_hits: List[str] = []

    for word in tokens:
        if word in POSITIVE_MARKERS:
            positive_hits.append(word)
        if word in DISTRESS_MARKERS:
            distress_hits.append(word)

    # Check cognitive rigidity with regex to catch variations like "غیرممکنه"
    for pattern in COGNITIVE_RIGIDITY_PATTERNS:
        matches = re.findall(pattern, normalized_text, flags=re.IGNORECASE)
        for m in matches:
            rigidity_hits.append(m)

    pos_count = len(positive_hits)
    dis_count = len(distress_hits)

    # Compute baseline stress indicator [0.0 - 1.0]
    raw_stress = (dis_count * 1.5) / (total_words + 5.0)
    stress_score = round(min(max(raw_stress * 4.0, 0.0), 1.0), 2)

    # Determine emotional valence
    if pos_count > dis_count:
        valence_label = "positive"
    elif dis_count > pos_count:
        valence_label = "distressed"
    else:
        valence_label = "neutral"

    has_rigidity = len(rigidity_hits) > 0
    all_cues = list(set(distress_hits + positive_hits + rigidity_hits))

    return {
        "stress_score": stress_score,
        "valence": valence_label,
        "detected_cues": all_cues,
        "cognitive_rigidity": has_rigidity
    }