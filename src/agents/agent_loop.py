"""
Universal agentic loop for the dating simulation.

All agent types (suitor, target, orchestrator) run through run_agent_loop().
The loop handles:
  - Dual-model strategy: Sonnet for turn-start calls, Haiku for tool-continuation
  - max_tool_calls cap: after N tool calls, force end_turn with tools disabled
  - tool_use block handling: all tool_result blocks for a single response go
    in one user message (Anthropic API requirement)
  - AgentLoopError on exhaustion: callers must catch and fall back

Anthropic API constraint:
  When the model returns multiple tool_use blocks in one response, ALL their
  tool_result blocks must appear in a single user message as a list of content
  blocks. This loop always batches them correctly.
"""

from __future__ import annotations
import json
from typing import Any, Callable

from config import MODEL, MODEL_FAST
from src.utils.llm_client import client


class AgentLoopError(Exception):
    """Raised when the agent loop exhausts max_iterations without end_turn."""
    pass


def run_agent_loop(
    system: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    tool_executor: Callable[[str, dict[str, Any]], dict[str, Any]],
    dialogue_model: str = MODEL,
    reasoning_model: str = MODEL_FAST,
    max_tool_calls: int = 2,
    max_iterations: int = 8,
    cacheable: bool = True,
    max_tokens: int = 1024,
) -> tuple[str, list[dict[str, Any]]]:
    """
    Run an agentic loop until the model produces a final text response.

    Dual-model strategy:
      - First call of each invocation uses dialogue_model (Sonnet).
        It may produce dialogue (end_turn) OR tool calls.
      - All subsequent calls within the same invocation (tool-continuation)
        use reasoning_model (Haiku) — the model is just deciding what to do
        next given tool results, not producing user-visible text.

    Tool call cap:
      After max_tool_calls cumulative tool calls, inject a "speak now" user
      message and remove tools from the next call. This forces end_turn on
      the next iteration.

    Args:
        system:          System prompt string. Cached if cacheable=True.
        messages:        Initial messages list (will be mutated — pass a copy
                         if you need to preserve the original).
        tools:           Anthropic tool schema list.
        tool_executor:   Callable(tool_name, tool_input) → result dict.
        dialogue_model:  Model for turn-start calls (default: Sonnet).
        reasoning_model: Model for tool-continuation calls (default: Haiku).
        max_tool_calls:  Max cumulative tool calls before forced end_turn.
        max_iterations:  Hard loop limit before AgentLoopError.
        cacheable:       Whether to apply cache_control to the system prompt.
        max_tokens:      Max tokens per API call.

    Returns:
        (final_text, full_message_history)
        final_text is the last text content block from the model.

    Raises:
        AgentLoopError: If max_iterations is reached without end_turn.
    """
    # Build the (possibly cached) system param
    if cacheable:
        system_param: str | list = [
            {"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}
        ]
    else:
        system_param = system

    tool_call_count = 0
    is_first_call = True

    for iteration in range(max_iterations):
        current_model = dialogue_model if is_first_call else reasoning_model
        is_first_call = False

        # If we've hit the tool cap, force end_turn by removing tools
        active_tools = tools if tool_call_count < max_tool_calls else []
        if tool_call_count >= max_tool_calls and active_tools == []:
            # Inject a directive so the model knows it must speak now
            messages.append({
                "role": "user",
                "content": (
                    "[System: You have used the maximum number of tools. "
                    "You must now produce your spoken dialogue line. "
                    "Do not call any more tools.]"
                ),
            })

        try:
            response = client.messages.create(
                model=current_model,
                max_tokens=max_tokens,
                system=system_param,
                messages=messages,
                tools=active_tools if active_tools else None,
            )
        except Exception as e:
            raise AgentLoopError(f"API call failed on iteration {iteration}: {e}") from e

        # Append the assistant turn to messages
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Extract the final text content block
            final_text = ""
            for block in response.content:
                if hasattr(block, "type") and block.type == "text":
                    final_text = block.text
                    break
                elif isinstance(block, dict) and block.get("type") == "text":
                    final_text = block["text"]
                    break
            return final_text, messages

        if response.stop_reason == "tool_use":
            # Collect ALL tool_use blocks from this response
            tool_use_blocks = [
                b for b in response.content
                if (hasattr(b, "type") and b.type == "tool_use")
                or (isinstance(b, dict) and b.get("type") == "tool_use")
            ]

            # Execute all tools and build a single user message with all results
            tool_result_contents: list[dict[str, Any]] = []
            for block in tool_use_blocks:
                if hasattr(block, "name"):
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id
                else:
                    tool_name = block["name"]
                    tool_input = block["input"]
                    tool_use_id = block["id"]

                try:
                    result = tool_executor(tool_name, tool_input)
                except Exception as e:
                    result = {"error": f"Tool execution failed: {e}"}

                tool_result_contents.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": json.dumps(result),
                })
                tool_call_count += 1

            # All tool_result blocks go in a single user message
            messages.append({"role": "user", "content": tool_result_contents})
            continue

        # stop_reason is something else (max_tokens, stop_sequence, etc.)
        # Try to extract text anyway before giving up
        for block in response.content:
            if hasattr(block, "type") and block.type == "text":
                return block.text, messages
            elif isinstance(block, dict) and block.get("type") == "text":
                return block["text"], messages

        raise AgentLoopError(
            f"Unexpected stop_reason '{response.stop_reason}' on iteration {iteration}."
        )

    raise AgentLoopError(
        f"Agent loop exhausted {max_iterations} iterations without end_turn. "
        f"Tool calls made: {tool_call_count}."
    )
