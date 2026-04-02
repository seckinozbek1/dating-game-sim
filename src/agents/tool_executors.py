"""
Tool execution layer for the agentic simulation.

Each executor class handles tool dispatch for one agent type.
These are the only places that import from the frozen scoring modules
(compatibility.py, selection.py) in the agentic code path.

read_body_language() uses a pure-Python word-list heuristic — no API call.
evaluate_match() is called by the orchestrator executor via dynamics.py.
"""

from __future__ import annotations
from typing import Any

from src.agents.conversation_state import ConversationState, SimulationState
from src.models.compatibility import compute_compatibility
from src.models.selection import svr_total


# ---------------------------------------------------------------------------
# Sentiment word lists for read_body_language()
# Based on LIWC positive/negative affect categories (Pennebaker et al., 2001)
# No external call — pure heuristic sufficient for engagement signal.
# ---------------------------------------------------------------------------
_POSITIVE_WORDS = {
    "interesting", "fascinating", "love", "great", "wonderful", "yes",
    "absolutely", "exactly", "brilliant", "curious", "surprising", "genuinely",
    "actually", "remarkable", "refreshing", "unexpected", "like", "enjoy",
    "appreciate", "good", "impressive", "agree", "excited", "intriguing",
    "tell", "more", "please", "laugh", "smile", "warm", "beautiful",
}
_NEGATIVE_WORDS = {
    "boring", "tired", "whatever", "fine", "maybe", "hmm", "anyway",
    "suppose", "guess", "sure", "okay", "alright", "not really", "no",
    "actually", "unfortunately", "busy", "late", "excuse", "sorry",
    "must", "should", "need", "go", "elsewhere", "somewhere", "other",
}

# "actually" appears in both; negative context usually dominates so kept


def _score_sentiment(text: str) -> tuple[float, str]:
    """
    Compute engagement score from Vera's last message text.

    Returns (score: 0.0–1.0, label: str).
    Labels: 'withdrawn' (0–0.25), 'polite' (0.25–0.50),
            'engaged' (0.50–0.75), 'enthusiastic' (0.75–1.0).
    """
    words = text.lower().split()
    word_set = set(words)
    pos = sum(1 for w in words if w in _POSITIVE_WORDS)
    neg = sum(1 for w in words if w in _NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        score = 0.45  # Neutral — short/ambiguous response
    else:
        score = pos / total

    # Clamp and map to label
    score = max(0.0, min(1.0, score))
    if score < 0.25:
        label = "withdrawn"
    elif score < 0.50:
        label = "polite"
    elif score < 0.75:
        label = "engaged"
    else:
        label = "enthusiastic"

    return round(score, 3), label


# ---------------------------------------------------------------------------
# Suitor tool executor
# ---------------------------------------------------------------------------

class SuitorToolExecutor:
    """
    Executes tool calls on behalf of a suitor agent.

    Holds references to the suitor's data, the target's data, and the
    current ConversationState so tool results reflect live simulation state.
    """

    def __init__(
        self,
        suitor: dict[str, Any],
        target: dict[str, Any],
        state: ConversationState,
        all_agents: dict[str, dict[str, Any]],
    ) -> None:
        self.suitor = suitor
        self.target = target
        self.state = state
        self.all_agents = all_agents  # id → agent dict, for target lookup

    def execute(self, tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
        """Dispatch a tool call by name. Returns a JSON-serializable result dict."""
        if tool_name == "check_compatibility":
            return self._check_compatibility(tool_input.get("target_id", "T"))
        elif tool_name == "change_strategy":
            return self._change_strategy(tool_input["new_strategy"])
        elif tool_name == "read_body_language":
            return self._read_body_language()
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _check_compatibility(self, target_id: str) -> dict[str, Any]:
        """
        Wraps compute_compatibility() + svr_total() from frozen scoring modules.
        Uses the suitor's current in-session strategy (may differ from personas.json
        if change_strategy was called earlier this encounter).
        """
        # Build a copy of suitor with current session strategy
        suitor_snapshot = {**self.suitor, "strategy": self.state.current_strategy}
        compat = compute_compatibility(suitor_snapshot, self.target)
        svr = svr_total(suitor_snapshot, self.target)
        return {
            "compatibility": compat,
            "svr": svr,
            "interpretation": _interpret_compat(compat["overall"]),
        }

    def _change_strategy(self, new_strategy: str) -> dict[str, Any]:
        """
        Mutates the suitor's in-session strategy. Never persists to personas.json.
        """
        old = self.state.current_strategy
        self.state.current_strategy = new_strategy
        return {
            "updated": True,
            "previous_strategy": old,
            "current_strategy": new_strategy,
        }

    def _read_body_language(self) -> dict[str, Any]:
        """
        Returns Vera's engagement level based on her last message.
        Pure Python word-list heuristic — no API call (Pennebaker et al., 2001).
        """
        text = self.state.vera_last_message
        if not text:
            return {"engagement": 0.5, "label": "polite", "note": "No response yet."}
        score, label = _score_sentiment(text)
        return {"engagement": score, "label": label}


def _interpret_compat(overall: float) -> str:
    if overall >= 0.75:
        return "Strong match — high compatibility across dimensions."
    elif overall >= 0.55:
        return "Moderate match — meaningful overlap with some friction points."
    elif overall >= 0.40:
        return "Weak match — notable misalignment; consider adjusting strategy."
    else:
        return "Poor match — fundamental incompatibility. Manage expectations."


# ---------------------------------------------------------------------------
# Target (Vera) tool executor
# ---------------------------------------------------------------------------

class TargetToolExecutor:
    """Executes tool calls on behalf of the target agent (Vera)."""

    def __init__(self, state: ConversationState) -> None:
        self.state = state

    def execute(self, tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
        if tool_name == "end_conversation_early":
            return self._end_conversation_early(tool_input.get("reason", ""))
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _end_conversation_early(self, reason: str) -> dict[str, Any]:
        """
        Sets the early_exit flag on ConversationState.
        The agent loop in agentic_main checks this flag after each Vera turn.
        """
        self.state.early_exit = True
        self.state.early_exit_reason = reason
        return {"ended": True, "reason": reason}


# ---------------------------------------------------------------------------
# Orchestrator tool executor
# ---------------------------------------------------------------------------

class OrchestratorToolExecutor:
    """
    Executes tool calls on behalf of the orchestrator agent.

    Holds a reference to the full SimulationState so it can inject events
    and look up encounter results. The evaluator call is deferred to
    agentic_main to avoid circular imports.
    """

    def __init__(
        self,
        sim_state: SimulationState,
        target: dict[str, Any],
        all_suitors: list[dict[str, Any]],
        evaluator_callback: Any,  # Callable[[str], dict] injected by agentic_main
    ) -> None:
        self.sim_state = sim_state
        self.target = target
        self.suitor_map: dict[str, dict[str, Any]] = {s["id"]: s for s in all_suitors}
        self._evaluator_callback = evaluator_callback

    def execute(self, tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
        if tool_name == "introduce_event":
            return self._introduce_event(
                tool_input["event_type"],
                tool_input["affects_suitor_id"],
            )
        elif tool_name == "call_evaluator":
            return self._call_evaluator(tool_input["chosen_suitor_id"])
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _introduce_event(self, event_type: str, affects_suitor_id: str) -> dict[str, Any]:
        """Queue an environmental event for the next encounter."""
        self.sim_state.pending_events.append(event_type)
        return {"injected": True, "event": event_type, "for_suitor": affects_suitor_id}

    def _call_evaluator(self, chosen_suitor_id: str) -> dict[str, Any]:
        """
        Invoke the relationship evaluator via the callback injected by agentic_main.
        The callback has the full conversation context available.
        """
        return self._evaluator_callback(chosen_suitor_id)
