"""
Mate selection engine.

Implements Murstein's Stimulus-Value-Role (SVR) Theory (1970):
- Stage 1 (Stimulus): Initial attraction based on observable traits
- Stage 2 (Value): Compatibility on values and personality
- Stage 3 (Role): Functional fit in relationship roles

Also implements Li et al. (2002) necessities vs luxuries budget model.
"""

from __future__ import annotations
from typing import Any
from src.models.compatibility import cosine_similarity


# Li et al. (2002): necessities are prioritized under resource constraints
NECESSITY_TRAITS = {"kindness", "intelligence", "stability"}
LUXURY_TRAITS = {"attractiveness", "status", "humor"}


def stimulus_score(agent1: dict[str, Any], agent2: dict[str, Any]) -> float:
    """
    Stage 1: Stimulus — initial attraction from observable traits.
    Weighted toward attractiveness, humor, extraversion (what you notice first).
    """
    obs_traits_1 = {
        "attractiveness": agent2["traits"]["attractiveness"],
        "humor": agent2["traits"]["humor"],
        "extraversion": agent2["big5"]["extraversion"],
    }
    obs_traits_2 = {
        "attractiveness": agent1["traits"]["attractiveness"],
        "humor": agent1["traits"]["humor"],
        "extraversion": agent1["big5"]["extraversion"],
    }
    # Average of how attractive each finds the other's observable traits
    score1 = sum(obs_traits_1.values()) / (len(obs_traits_1) * 100)
    score2 = sum(obs_traits_2.values()) / (len(obs_traits_2) * 100)
    return (score1 + score2) / 2


def value_score(agent1: dict[str, Any], agent2: dict[str, Any]) -> float:
    """
    Stage 2: Value — compatibility on deeper values and personality.
    Uses Big Five similarity as proxy for value alignment.
    """
    return cosine_similarity(agent1["big5"], agent2["big5"])


def role_score(agent1: dict[str, Any], agent2: dict[str, Any]) -> float:
    """
    Stage 3: Role — functional fit in relationship roles.
    Strategy alignment + complementary conscientiousness.
    """
    strategy_match = 1.0 if agent1["strategy"] == agent2["strategy"] else 0.3
    # Complementarity on conscientiousness (one planner + one spontaneous can work)
    consc_diff = abs(agent1["big5"]["conscientiousness"] - agent2["big5"]["conscientiousness"])
    consc_complement = 1.0 - (consc_diff / 200)  # Mild preference for similarity
    return strategy_match * 0.7 + consc_complement * 0.3


def necessity_luxury_score(agent: dict[str, Any]) -> dict[str, float]:
    """
    Li et al. (2002) budget model: what does this agent prioritize?
    Returns separate scores for necessities and luxuries.
    """
    necessity_avg = sum(agent["traits"][t] for t in NECESSITY_TRAITS) / len(NECESSITY_TRAITS)
    luxury_avg = sum(agent["traits"][t] for t in LUXURY_TRAITS) / len(LUXURY_TRAITS)
    return {
        "necessity_score": round(necessity_avg / 100, 3),
        "luxury_score": round(luxury_avg / 100, 3),
    }


def svr_total(agent1: dict[str, Any], agent2: dict[str, Any]) -> dict[str, float]:
    """
    Full SVR score combining all three stages.
    Weights: Stimulus 0.3, Value 0.4, Role 0.3
    (Value weighted highest per Murstein's finding that it's most predictive for LTR)
    """
    s = stimulus_score(agent1, agent2)
    v = value_score(agent1, agent2)
    r = role_score(agent1, agent2)
    total = s * 0.3 + v * 0.4 + r * 0.3
    return {
        "stimulus": round(s, 3),
        "value": round(v, 3),
        "role": round(r, 3),
        "svr_total": round(total, 3),
    }
