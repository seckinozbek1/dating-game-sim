"""
Shared Anthropic client and call_llm utility.

Extracted from dynamics.py so both dynamics.py (non-agentic path) and
tool_executors.py / agent_loop.py (agentic path) can import without
creating a circular dependency.

Prompt caching:
  Pass cacheable=True to wrap the system prompt in a content block with
  cache_control={"type": "ephemeral"}. This gives a ~90% discount on
  repeated input tokens (personality profiles, evaluator prompts).
  Cache TTL is 5 minutes, reset on each use.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure project root is on path when this module is imported standalone
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, MODEL

client = Anthropic(api_key=ANTHROPIC_API_KEY)


def call_llm(
    system: str,
    user_message: str,
    model: str = MODEL,
    cacheable: bool = False,
    max_tokens: int = 1024,
) -> str:
    """
    Make a single LLM call with optional prompt caching.

    Args:
        system:       System prompt text.
        user_message: The user turn content.
        model:        Model ID. Defaults to MODEL (Sonnet) from config.
        cacheable:    When True, wraps the system prompt in a cache_control
                      content block for Anthropic prompt caching.
                      Use for calls where the system prompt is identical
                      across multiple invocations (agent personas, evaluator).
        max_tokens:   Max tokens for the response.

    Returns:
        The model's text response, or an error string on failure.
    """
    try:
        if cacheable:
            system_param: str | list = [
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        else:
            system_param = system

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_param,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text
    except Exception as e:
        return f"[LLM call failed: {e}]"
