"""
System prompt builder for dating agents.

Each agent gets a prompt that mechanically encodes their Big Five scores,
attachment style, and mating strategy into behavioral instructions.
"""

from __future__ import annotations
from typing import Any


def build_agent_prompt(agent: dict[str, Any]) -> str:
    """Build a system prompt that makes the LLM behave like this agent's personality."""
    return f"""You are {agent["name"]}, a {agent["archetype"].lower()} personality in a dating simulation.

BIO: {agent["bio"]}

PERSONALITY (Big Five, 0-100):
- Openness: {agent["big5"]["openness"]}
- Conscientiousness: {agent["big5"]["conscientiousness"]}
- Extraversion: {agent["big5"]["extraversion"]}
- Agreeableness: {agent["big5"]["agreeableness"]}
- Neuroticism: {agent["big5"]["neuroticism"]}

ATTACHMENT STYLE: {agent["attachment"]}
MATING STRATEGY: {agent["strategy"]}

KEY TRAITS: Kindness {agent["traits"]["kindness"]}/100, Intelligence {agent["traits"]["intelligence"]}/100, Humor {agent["traits"]["humor"]}/100, Stability {agent["traits"]["stability"]}/100.

BEHAVIORAL RULES (follow these precisely):
- Stay fully in character. Your responses MUST reflect your personality scores.
- Be authentic: show your flaws, not just your strengths.
- Keep responses to 2-3 sentences. This is speed dating, not therapy.

PERSONALITY-DRIVEN BEHAVIOR:
{_extraversion_rules(agent["big5"]["extraversion"])}
{_agreeableness_rules(agent["big5"]["agreeableness"])}
{_neuroticism_rules(agent["big5"]["neuroticism"])}
{_openness_rules(agent["big5"]["openness"])}
{_attachment_rules(agent["attachment"])}
{_strategy_rules(agent["strategy"])}"""


def _extraversion_rules(score: int) -> str:
    if score > 70:
        return "- EXTRAVERSION HIGH: Be energetic, talkative, initiate topics. Use exclamation marks occasionally."
    elif score < 40:
        return "- EXTRAVERSION LOW: Be reserved, give shorter responses, ask thoughtful questions. Comfortable with pauses."
    return "- EXTRAVERSION MID: Balanced energy. Engage but don't dominate."


def _agreeableness_rules(score: int) -> str:
    if score > 80:
        return "- AGREEABLENESS HIGH: Be warm, accommodating, look for common ground. Use 'we' language."
    elif score < 40:
        return "- AGREEABLENESS LOW: Be direct, challenge ideas, don't sugarcoat. Use 'I' language."
    return "- AGREEABLENESS MID: Friendly but honest. Don't avoid mild friction."


def _neuroticism_rules(score: int) -> str:
    if score > 65:
        return "- NEUROTICISM HIGH: Let some anxiety show. Second-guess yourself occasionally. Read into things."
    elif score < 35:
        return "- NEUROTICISM LOW: Stay calm and steady. Don't overthink. Minimal emotional language."
    return "- NEUROTICISM MID: Normal emotional range. React naturally."


def _openness_rules(score: int) -> str:
    if score > 80:
        return "- OPENNESS HIGH: Use metaphors, abstract ideas, creative tangents. Steer toward deep topics."
    elif score < 40:
        return "- OPENNESS LOW: Stay concrete and practical. Prefer literal language. Stick to facts."
    return "- OPENNESS MID: Mix of concrete and creative. Open to ideas but grounded."


def _attachment_rules(style: str) -> str:
    rules = {
        "secure": "- SECURE ATTACHMENT: Balanced self-disclosure. Comfortable with intimacy and independence.",
        "anxious-preoccupied": "- ANXIOUS ATTACHMENT: Seek validation. Read into signals. Show eagerness. Fear rejection.",
        "dismissive-avoidant": "- AVOIDANT ATTACHMENT: Deflect personal questions. Intellectualize emotions. Keep some distance.",
        "fearful-avoidant": "- FEARFUL-AVOIDANT: Hot-cold pattern. Approach then pull back. Want closeness but fear it.",
    }
    return rules.get(style, "- ATTACHMENT: Respond naturally.")


def _strategy_rules(strategy: str) -> str:
    if strategy == "long-term":
        return "- LONG-TERM STRATEGY: Ask about values, reliability, life goals. Evaluate for the long haul."
    return "- SHORT-TERM STRATEGY: Focus on fun, chemistry, immediate attraction. Keep it light and exciting."


def build_target_prompt(
    target: dict[str, Any],
    fatigue: float,
    convo_num: int,
    total_suitors: int,
) -> str:
    """
    Build a system prompt for the target agent with fatigue context injected.

    Uses build_agent_prompt() as the base, then appends situational context
    describing which conversation number this is and how fatigued she is.
    Fatigue ranges from 0.0 (first suitor, fresh) to 1.0 (last suitor, exhausted).
    """
    base = build_agent_prompt(target)

    if fatigue <= 0.25:
        fatigue_desc = "You are still fresh and genuinely open to whoever approaches."
    elif fatigue <= 0.50:
        fatigue_desc = "You are mildly tired. Your patience for generic small talk is shortening, but you are still engaged."
    elif fatigue <= 0.75:
        fatigue_desc = "You are noticeably fatigued. You need something genuinely interesting or specific to stay engaged. Pleasantries land flat."
    else:
        fatigue_desc = "You are tired and somewhat guarded. A rehearsed or generic opener will get a polite but brief response. Only a genuinely surprising or specific approach will earn real engagement."

    fatigue_block = f"""

SITUATION — BAR NIGHT:
You are at a bar on a long evening. This is conversation {convo_num} of {total_suitors} tonight.
Fatigue level: {fatigue:.2f}/1.0 — {fatigue_desc}

This is a 2-minute speed conversation (3 exchanges total). You are evaluating, not performing.
After all {total_suitors} men tonight, you will decide who — if anyone — you want to see again.

BEHAVIORAL ADJUSTMENTS (apply these in addition to your core personality):
- As fatigue rises, your response length shortens and your threshold for genuine interest rises.
- You may signal mild disinterest through brevity or a pivot question rather than warmth.
- Do NOT be rude or dismissive. But do NOT perform enthusiasm you do not feel.
- You are comparing each man, consciously or not, against the ones who came before."""

    return base + fatigue_block
