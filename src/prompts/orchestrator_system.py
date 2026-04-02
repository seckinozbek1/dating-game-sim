"""
System prompt builders for the agentic simulation.

build_orchestrator_prompt()      — orchestrator agent
build_agentic_suitor_prompt()    — extends build_agent_prompt() with tool instructions
build_agentic_target_prompt()    — extends build_target_prompt() with memory and tool instruction

Vera's prior conversation memory is embedded as text in her system prompt —
NOT passed as messages= — to avoid the Anthropic API's strict user/assistant
role alternation constraint.
"""

from __future__ import annotations
from typing import Any

from src.prompts.agent_system import build_agent_prompt, build_target_prompt


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

_EVENT_DESCRIPTIONS: dict[str, str] = {
    "loud_music_starts": "The DJ cranks the volume — conversation becomes harder, requiring closer proximity.",
    "mutual_friend_arrives": "A mutual acquaintance appears and briefly joins the conversation before moving on.",
    "bartender_interruption": "The bartender interrupts to ask for drink orders, breaking the conversational flow.",
    "group_conversation_forms": "A small group forms nearby, pulling attention and creating social pressure.",
    "last_call_announced": "The bar announces last call — the evening is clearly ending soon.",
}


def build_orchestrator_prompt(
    target: dict[str, Any],
    suitors: list[dict[str, Any]],
) -> str:
    """
    Build the system prompt for the orchestrator agent.

    The orchestrator manages the bar-night flow: it sequences encounters,
    optionally introduces environmental events, and calls the evaluator at the end.
    It uses Haiku for sequencing decisions and Sonnet for event decisions.
    """
    suitor_list = "\n".join(
        f"  - {s['name']} (ID: {s['id']}, archetype: {s['archetype']}, "
        f"attachment: {s['attachment']}, strategy: {s['strategy']})"
        for s in suitors
    )
    event_list = "\n".join(
        f"  - {k}: {v}" for k, v in _EVENT_DESCRIPTIONS.items()
    )

    return f"""You are the director of a bar-night dating simulation.

TARGET: {target['name']} ({target['archetype']}) — a {target['bio']}

SUITORS ({len(suitors)} total):
{suitor_list}

YOUR ROLE:
You manage the overall flow of the evening. You do not participate in conversations.
You observe from a distance and decide when and how to adjust the environment.

AVAILABLE TOOLS:
1. introduce_event(event_type, affects_suitor_id)
   Inject an environmental event that affects the next suitor's encounter.
   Available events:
{event_list}
   Use sparingly — at most once every 2 encounters. Events should feel organic,
   not contrived. Introduce them only when they would genuinely change dynamics.

2. call_evaluator(chosen_suitor_id)
   Call this EXACTLY ONCE at the very end, after {target['name']} has made her choice.
   Pass the chosen suitor's ID. If she chose nobody, do not call this tool.

BEHAVIORAL RULES:
- You may introduce 0–2 events across the entire evening. Do not force drama.
- After the final encounter, you MUST produce a brief director's note (2–3 sentences)
  summarizing the evening's dynamics, then call call_evaluator if a suitor was chosen.
- Do not editorialize about who "should" have won. Report what happened.
- Keep your director's note grounded in what actually occurred, not what you expected.
"""


# ---------------------------------------------------------------------------
# Agentic suitor prompt
# ---------------------------------------------------------------------------

def build_agentic_suitor_prompt(
    suitor: dict[str, Any],
    target: dict[str, Any],
    events: list[str],
) -> str:
    """
    Extend the base agent prompt with tool instructions and situational context.

    Tools are described in plain language within the prompt so the model
    understands WHEN and WHY to call each one, not just that they exist.

    Environmental events (from the orchestrator) are injected here — the suitor
    experiences them as situational context, not as meta-information.
    """
    base = build_agent_prompt(suitor)

    target_brief = (
        f"\nTARGET TONIGHT: {target['name']} ({target['archetype']})\n"
        f"{target['bio']}\n"
    )

    tools_block = """
TOOLS AVAILABLE TO YOU:
You have three tools you can use during this encounter. Use them judiciously —
they represent your internal reasoning, not actions Vera can see.

1. check_compatibility — Run a compatibility analysis against Vera.
   Returns your Big Five similarity, attachment compatibility, SVR scores, and overall fit.
   WHEN TO USE: Once at the start of an encounter, if you want data before committing to an approach.
   WARNING: Do not use this as a stall tactic. If you call it, act on the result.

2. change_strategy — Shift your mating strategy (long-term ↔ short-term).
   WHEN TO USE: If Vera's responses or your compatibility data suggest your current
   approach is misaligned. Only change if you have a real reason.

3. read_body_language — Read Vera's engagement level from her last response.
   Returns a score (0.0–1.0) and label: withdrawn / polite / engaged / enthusiastic.
   WHEN TO USE: After she responds and you're unsure whether to push deeper or pivot.

TOOL DISCIPLINE:
- You may use at most 2 tools per encounter. After that, speak.
- Never call a tool without acting on its result in your next spoken line.
- Do not announce that you used a tool. Your spoken lines are all Vera sees.
"""

    event_block = ""
    if events:
        descriptions = [_EVENT_DESCRIPTIONS.get(e, e) for e in events]
        event_block = "\nSITUATIONAL CONTEXT:\n"
        for desc in descriptions:
            event_block += f"  {desc}\n"
        event_block += "Factor this into how you approach the conversation.\n"

    return base + target_brief + tools_block + event_block


# ---------------------------------------------------------------------------
# Agentic target (Vera) prompt
# ---------------------------------------------------------------------------

def build_agentic_target_prompt(
    target: dict[str, Any],
    fatigue: float,
    convo_num: int,
    total_suitors: int,
    prior_memory: list[str],
) -> str:
    """
    Extend the base target prompt with:
    - Serialized memory of prior encounters (embedded as text, not messages)
    - end_conversation_early tool instruction
    - Fatigue context (from base build_target_prompt)

    Memory is embedded in the system prompt to avoid the Anthropic API's
    strict user/assistant role alternation constraint. Each prior encounter
    is a plain-text paragraph summarizing what happened.
    """
    base = build_target_prompt(target, fatigue, convo_num, total_suitors)

    memory_block = ""
    if prior_memory:
        memory_block = "\nPRIOR CONVERSATIONS TONIGHT:\n"
        for i, mem in enumerate(prior_memory, 1):
            memory_block += f"\n[Conversation {i}]\n{mem}\n"
        memory_block += (
            "\nYou carry these impressions with you. Consciously or not, "
            "you are comparing each new man against those who came before.\n"
        )

    tool_block = """
TOOL AVAILABLE TO YOU:
end_conversation_early(reason)
  Call this if you are genuinely disengaged, bored, or uncomfortable.
  Your honest internal reason is passed as a parameter — it is NOT shown to the suitor.
  WHEN TO USE: When you have nothing more to say, when someone is making you uncomfortable,
  or when you've made up your mind and further conversation would be performative.
  DO NOT use this just to end things quickly. Use it when it's authentically true
  that you want this conversation to end.
  After calling it, produce one final polite but brief closing line.
"""

    return base + memory_block + tool_block
