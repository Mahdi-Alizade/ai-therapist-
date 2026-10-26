import re
from typing import Dict, List, Any

# Emotional and Cognitive Lexicon Markers
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

COGNITIVE_RIGIDITY_MARKERS = {
    "always", "never", "must", "should", "ruined", "impossible", "failed",
    "همیشه", "هرگز", "باید", "حتما", "نابود", "غیرممکن", "شکست"
}


def analyze_text_sentiment(text: str) -> Dict[str, Any]:
    """
    Evaluates emotional valence, stress index, and cognitive rigidity cues
    from the user's conversational text.
    """
    clean_text = text.lower().replace("\u200c", " ")
    tokens = re.findall(r"\b\w+\b", clean_text, flags=re.UNICODE)

    total_words = len(tokens)
    if total_words == 0:
        return {
            "stress_score": 0.0,
            "valence": "neutral",
            "detected_cues": [],
            "cognitive_rigidity": False
        }

    positive_hits: List[str] = []
    distress_hits: List[str] = []
    rigidity_hits: List[str] = []

    for word in tokens:
        if word in POSITIVE_MARKERS:
            positive_hits.append(word)
        if word in DISTRESS_MARKERS:
            distress_hits.append(word)
        if word in COGNITIVE_RIGIDITY_MARKERS:
            rigidity_hits.append(word)

    pos_count = len(positive_hits)
    dis_count = len(distress_hits)

    # Compute baseline stress indicator [0.0 - 1.0]
    raw_stress = (dis_count * 1.5) / (total_words + 5.0)
    stress_score = round(min(max(raw_stress * 4.0, 0.0), 1.0), 2)

    # Compute Valence
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