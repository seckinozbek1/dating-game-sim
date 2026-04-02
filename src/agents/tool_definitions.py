"""
Anthropic tool schemas for all agent types.

These dicts are passed directly as the tools= parameter to client.messages.create().
No logic lives here — only schema definitions.

Descriptions are written from each agent's first-person perspective so
the model understands when and why to call each tool.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Suitor tools
# ---------------------------------------------------------------------------

SUITOR_TOOLS: list[dict] = [
    {
        "name": "check_compatibility",
        "description": (
            "Run a compatibility analysis between yourself and Vera. "
            "Returns your Big Five similarity, attachment compatibility, "
            "SVR stage scores (stimulus / value / role), and an overall score. "
            "Use this once at the start of an encounter to calibrate your approach."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "target_id": {
                    "type": "string",
                    "description": "The target's agent ID. Always 'T' for Vera.",
                }
            },
            "required": ["target_id"],
        },
    },
    {
        "name": "change_strategy",
        "description": (
            "Shift your mating strategy for the rest of this encounter. "
            "Use this if the compatibility data or Vera's responses suggest "
            "your current approach is misaligned. "
            "Valid values: 'long-term' or 'short-term'."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "new_strategy": {
                    "type": "string",
                    "enum": ["long-term", "short-term"],
                    "description": "The strategy to switch to.",
                }
            },
            "required": ["new_strategy"],
        },
    },
    {
        "name": "read_body_language",
        "description": (
            "Read Vera's current engagement level based on her last response. "
            "Returns an engagement score (0.0–1.0) and a label: "
            "'withdrawn', 'polite', 'engaged', or 'enthusiastic'. "
            "Use this after she responds to decide whether to press forward, "
            "pivot topics, or cut your losses."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]


# ---------------------------------------------------------------------------
# Target (Vera) tools
# ---------------------------------------------------------------------------

TARGET_TOOLS: list[dict] = [
    {
        "name": "end_conversation_early",
        "description": (
            "End this conversation before the scheduled 3 exchanges are complete. "
            "Call this if the suitor is boring, making you uncomfortable, "
            "or if you have genuinely nothing more to say. "
            "Be honest with yourself — do not end early out of politeness, "
            "only out of authentic disengagement or discomfort."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": (
                        "Your internal reason for ending early. "
                        "Not shown to the suitor — this is your honest assessment."
                    ),
                }
            },
            "required": ["reason"],
        },
    },
]


# ---------------------------------------------------------------------------
# Orchestrator tools
# ---------------------------------------------------------------------------

ORCHESTRATOR_TOOLS: list[dict] = [
    {
        "name": "introduce_event",
        "description": (
            "Inject an environmental event that will affect the next suitor's encounter. "
            "Events add situational pressure or opportunity to the bar setting. "
            "Use sparingly — at most once every 2 encounters."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "event_type": {
                    "type": "string",
                    "enum": [
                        "loud_music_starts",
                        "mutual_friend_arrives",
                        "bartender_interruption",
                        "group_conversation_forms",
                        "last_call_announced",
                    ],
                    "description": "The type of environmental event to introduce.",
                },
                "affects_suitor_id": {
                    "type": "string",
                    "description": "The suitor ID whose next encounter this event affects (e.g. 'S3').",
                },
            },
            "required": ["event_type", "affects_suitor_id"],
        },
    },
    {
        "name": "call_evaluator",
        "description": (
            "Invoke the relationship evaluator to produce a final psychologist's verdict "
            "on the chosen pairing. Call this exactly once, after all encounters are complete "
            "and Vera has chosen a suitor. Pass the chosen suitor's ID."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "chosen_suitor_id": {
                    "type": "string",
                    "description": "The ID of the suitor Vera chose (e.g. 'S1').",
                }
            },
            "required": ["chosen_suitor_id"],
        },
    },
]
