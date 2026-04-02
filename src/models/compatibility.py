"""
Compatibility and relationship quality scoring.

Theories implemented:
- Assortative mating via cosine similarity (Thiessen & Gregg, 1980)
- Attachment compatibility matrix (Hazan & Shaver, 1987; Kirkpatrick & Davis, 1994)
- Gottman's Four Horsemen (Gottman et al., 1998)
- Positive/negative interaction ratio (Gottman, 1994)
"""

from __future__ import annotations
import math
from typing import Any


# Empirical attachment compatibility matrix
# Values represent expected relationship quality (0-1)
# Based on Hazan & Shaver (1987) and Kirkpatrick & Davis (1994)
ATTACHMENT_COMPAT: dict[str, float] = {
    "secure+secure": 0.95,
    "secure+anxious-preoccupied": 0.65,
    "secure+dismissive-avoidant": 0.60,
    "secure+fearful-avoidant": 0.50,
    "anxious-preoccupied+dismissive-avoidant": 0.25,  # Classic trap
    "anxious-preoccupied+anxious-preoccupied": 0.40,
    "dismissive-avoidant+dismissive-avoidant": 0.35,
    "anxious-preoccupied+fearful-avoidant": 0.30,
    "dismissive-avoidant+fearful-avoidant": 0.30,
    "fearful-avoidant+fearful-avoidant": 0.20,
}


def cosine_similarity(v1: dict[str, float], v2: dict[str, float]) -> float:
    """Cosine similarity between two trait dictionaries."""
    keys = v1.keys()
    dot = sum(v1[k] * v2[k] for k in keys)
    mag1 = math.sqrt(sum(v1[k] ** 2 for k in keys))
    mag2 = math.sqrt(sum(v2[k] ** 2 for k in keys))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def get_attachment_score(a1: str, a2: str) -> float:
    """Look up attachment compatibility from empirical matrix."""
    key1 = f"{a1}+{a2}"
    key2 = f"{a2}+{a1}"
    return ATTACHMENT_COMPAT.get(key1, ATTACHMENT_COMPAT.get(key2, 0.5))


def compute_compatibility(agent1: dict[str, Any], agent2: dict[str, Any]) -> dict[str, float]:
    """
    Compute multi-dimensional compatibility score.

    Weights justified by:
    - Attachment: 0.35 (strongest predictor per Hazan & Shaver, 1987)
    - Big Five similarity: 0.25 (assortative mating, moderate predictor)
    - Strategy alignment: 0.20 (Buss & Schmitt, 1993: mismatch is costly)
    - Trait similarity: 0.20 (Li et al., 2002: secondary to attachment)
    """
    big5_sim = cosine_similarity(agent1["big5"], agent2["big5"])
    trait_sim = cosine_similarity(agent1["traits"], agent2["traits"])
    attach_score = get_attachment_score(agent1["attachment"], agent2["attachment"])
    strategy_match = 1.0 if agent1["strategy"] == agent2["strategy"] else 0.4

    overall = (
        big5_sim * 0.25
        + trait_sim * 0.20
        + attach_score * 0.35
        + strategy_match * 0.20
    )

    return {
        "big5_similarity": round(big5_sim, 3),
        "trait_similarity": round(trait_sim, 3),
        "attachment_compat": round(attach_score, 3),
        "strategy_match": round(strategy_match, 3),
        "overall": round(overall, 3),
    }


def predict_gottman(
    agent1: dict[str, Any],
    agent2: dict[str, Any],
    compat: dict[str, float],
) -> dict[str, Any]:
    """
    Predict relationship stability using Gottman-derived heuristics.

    Four Horsemen (Gottman et al., 1998):
    - Criticism: attacks on partner's character (driven by neuroticism + low agreeableness)
    - Contempt: superiority/disgust (driven by low attachment compat + neuroticism)
    - Defensiveness: self-protection (driven by neuroticism + low agreeableness)
    - Stonewalling: emotional withdrawal (driven by low stability + avoidant attachment)

    5:1 Ratio (Gottman, 1994):
    - Stable couples maintain ≥5 positive interactions per negative one.
    """
    neuro_avg = (agent1["big5"]["neuroticism"] + agent2["big5"]["neuroticism"]) / 200
    agree_avg = (agent1["big5"]["agreeableness"] + agent2["big5"]["agreeableness"]) / 200
    stab_avg = (agent1["traits"]["stability"] + agent2["traits"]["stability"]) / 200

    has_avoidant = (
        agent1["attachment"] == "dismissive-avoidant"
        or agent2["attachment"] == "dismissive-avoidant"
    )

    # Four Horsemen risk scores (0-1, higher = more risk)
    criticism = min(1.0, neuro_avg * 1.3 * (1 - agree_avg))
    contempt = min(1.0, (1 - compat["attachment_compat"]) * 0.8 + neuro_avg * 0.3)
    defensiveness = min(1.0, neuro_avg * 0.7 + (1 - agree_avg) * 0.5)
    stonewalling = min(1.0, (1 - stab_avg) * 0.5 + (0.4 if has_avoidant else 0.0))

    horsemen_avg = (criticism + contempt + defensiveness + stonewalling) / 4

    # Positive/negative ratio proxy
    positive = (agree_avg * 3 + stab_avg * 2 + compat["overall"] * 3) / 8
    negative = horsemen_avg
    ratio = positive / negative if negative > 0.01 else 10.0

    # Stability score (0-100)
    stability = min(100, max(0,
        compat["overall"] * 40
        + (30 if ratio >= 5 else 20 if ratio >= 3 else 10 if ratio >= 1 else 0)
        + (1 - horsemen_avg) * 30
    ))

    if stability >= 75:
        prediction = "Likely stable"
    elif stability >= 50:
        prediction = "At risk"
    else:
        prediction = "Likely to dissolve"

    return {
        "four_horsemen": {
            "criticism": round(criticism, 3),
            "contempt": round(contempt, 3),
            "defensiveness": round(defensiveness, 3),
            "stonewalling": round(stonewalling, 3),
        },
        "positive_negative_ratio": round(ratio, 2),
        "stability_score": round(stability, 1),
        "prediction": prediction,
    }
