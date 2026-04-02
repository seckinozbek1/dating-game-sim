"""
Mutable state containers for the agentic simulation.

ConversationState — per-encounter scope (one suitor × Vera).
SimulationState   — full bar-night scope (all 5 encounters).

These are plain dataclasses (no logic) so they can be threaded through
agent loops and tool executors without coupling those modules together.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConversationState:
    """
    State that lives for exactly one suitor–Vera encounter.

    Mutated by:
    - SuitorToolExecutor._change_strategy()  → current_strategy
    - SuitorToolExecutor (reads)             → vera_last_message
    - TargetToolExecutor._end_conversation_early() → early_exit
    - agent_loop                             → tool_call_count
    """
    suitor_id: str
    vera_last_message: str = ""
    early_exit: bool = False
    early_exit_reason: str = ""
    tool_call_count: int = 0        # cumulative across all loop iterations this encounter
    current_strategy: str = ""      # starts from suitor's default, mutable via change_strategy
    exchange_count: int = 0         # number of completed dialogue exchanges


@dataclass
class SimulationState:
    """
    State that lives for the full bar-night run.

    vera_memory accumulates plain-text summaries of prior encounters,
    embedded in Vera's system prompt (NOT passed as messages= to avoid
    role-alternation constraint in the Anthropic API).

    pending_events holds event strings queued by the orchestrator to be
    consumed and injected into the next suitor's context, then cleared.
    """
    vera_memory: list[str] = field(default_factory=list)
    pending_events: list[str] = field(default_factory=list)
    encounter_transcripts: list[dict[str, Any]] = field(default_factory=list)
    suitor_results: dict[str, dict[str, Any]] = field(default_factory=dict)
