"""
Agentic bar-night simulation.

Replaces the Python-controlled run_bar_night() loop with an agentic one
where each participant (suitors, Vera, orchestrator) is an autonomous LLM
with tool access.

Three-tier flow:
  Tier A — Orchestrator decides to start an encounter, optionally injects an event.
  Tier B — Per-encounter: suitor and Vera alternate agentic turns.
  Tier C — Orchestrator calls the evaluator after Vera's final ranking.

Returns the same dict shape as run_bar_night() so main.py's display layer,
build_enriched_bar_night(), and save_results() all work unchanged.

Cost optimizations applied:
  - Dual model: Sonnet for turn-start/dialogue, Haiku for tool-continuation
  - max_tool_calls=2 per suitor encounter
  - Prompt caching on all system prompts (cacheable=True)
  - Annotation is opt-in only (--annotate flag)
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from src.agents.agent_loop import run_agent_loop, AgentLoopError
from src.agents.conversation_state import ConversationState, SimulationState
from src.agents.tool_definitions import SUITOR_TOOLS, TARGET_TOOLS, ORCHESTRATOR_TOOLS
from src.agents.tool_executors import (
    SuitorToolExecutor,
    TargetToolExecutor,
    OrchestratorToolExecutor,
)
from src.prompts.orchestrator_system import (
    build_orchestrator_prompt,
    build_agentic_suitor_prompt,
    build_agentic_target_prompt,
)
from src.models.compatibility import compute_compatibility, predict_gottman
from src.models.selection import svr_total
from src.models.dynamics import evaluate_match, annotate_exchange
from src.utils.llm_client import call_llm
from config import MODEL, MODEL_FAST


# ---------------------------------------------------------------------------
# Memory utilities
# ---------------------------------------------------------------------------

def _summarize_encounter_for_memory(
    suitor: dict[str, Any],
    conversation: list[dict[str, Any]],
    early_exit: bool,
    early_exit_reason: str,
) -> str:
    """
    Produce a plain-text summary of one encounter for Vera's memory.
    Embedded in her system prompt — not passed as messages.
    """
    lines = [f"{suitor['name']} ({suitor['archetype']}) approached."]
    for turn in conversation:
        lines.append(f'  {turn["speaker"]}: "{turn["text"]}"')
    if early_exit:
        lines.append(f"[You ended this conversation early. Internal note: {early_exit_reason}]")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Per-encounter conversation engine
# ---------------------------------------------------------------------------

def _run_agentic_encounter(
    suitor: dict[str, Any],
    target: dict[str, Any],
    sim_state: SimulationState,
    convo_num: int,
    total_suitors: int,
    exchanges: int = 3,
    verbose: bool = False,
    annotate: bool = False,
) -> tuple[list[dict[str, Any]], ConversationState]:
    """
    Run one suitor–Vera encounter with both agents being agentic.

    The suitor and Vera alternate synchronously:
      1. Suitor runs agent loop → produces one spoken line (may use tools first)
      2. Vera's vera_last_message is updated
      3. Vera runs agent loop → produces one spoken line (may call end_conversation_early)
      4. If Vera's early_exit is set, break out of the exchange loop

    Returns (conversation_turns, final_ConversationState).
    """
    fatigue = (convo_num - 1) / max(total_suitors - 1, 1)

    state = ConversationState(
        suitor_id=suitor["id"],
        current_strategy=suitor["strategy"],
    )

    suitor_executor = SuitorToolExecutor(
        suitor=suitor,
        target=target,
        state=state,
        all_agents={target["id"]: target},
    )
    vera_executor = TargetToolExecutor(state=state)

    suitor_system = build_agentic_suitor_prompt(
        suitor, target, events=list(sim_state.pending_events)
    )
    # Consume events after building the suitor's context
    sim_state.pending_events.clear()

    vera_system = build_agentic_target_prompt(
        target=target,
        fatigue=fatigue,
        convo_num=convo_num,
        total_suitors=total_suitors,
        prior_memory=list(sim_state.vera_memory),
    )

    conversation: list[dict[str, Any]] = []

    # --- Suitor opens ---
    opener_prompt = (
        f"You are approaching {target['name']} ({target['archetype']}) at the bar. "
        f"This is your moment to make a first impression. Be yourself. "
        f"You may use your tools before speaking, or speak immediately."
    )
    suitor_messages = [{"role": "user", "content": opener_prompt}]

    try:
        suitor_line, suitor_messages = run_agent_loop(
            system=suitor_system,
            messages=suitor_messages,
            tools=SUITOR_TOOLS,
            tool_executor=suitor_executor.execute,
            max_tool_calls=2,
            cacheable=True,
        )
    except AgentLoopError as e:
        # Fallback: single non-agentic call
        suitor_line = call_llm(suitor_system, opener_prompt, model=MODEL)

    state.vera_last_message = ""  # No Vera response yet for opener
    turn: dict[str, Any] = {"speaker": suitor["name"], "text": suitor_line}
    if annotate:
        turn["analysis"] = annotate_exchange(suitor, target, suitor_line)
    conversation.append(turn)
    state.exchange_count += 1

    if verbose:
        print(f"\n  {suitor['name']}: {suitor_line}")

    # --- Alternating exchanges ---
    prev_suitor_line = suitor_line

    for i in range(exchanges - 1):
        # --- Vera's turn ---
        vera_messages = [
            {
                "role": "user",
                "content": (
                    f"{suitor['name']} ({suitor['archetype']}) just said:\n"
                    f'"{prev_suitor_line}"\n\n'
                    f"Respond. You may call end_conversation_early if you want this to end."
                ),
            }
        ]

        try:
            vera_line, vera_messages = run_agent_loop(
                system=vera_system,
                messages=vera_messages,
                tools=TARGET_TOOLS,
                tool_executor=vera_executor.execute,
                max_tool_calls=1,  # Vera only needs one tool call
                cacheable=True,
            )
        except AgentLoopError:
            vera_line = call_llm(vera_system, vera_messages[0]["content"], model=MODEL)

        state.vera_last_message = vera_line
        vera_turn: dict[str, Any] = {"speaker": target["name"], "text": vera_line}
        if annotate:
            vera_turn["analysis"] = annotate_exchange(target, suitor, vera_line)
        conversation.append(vera_turn)

        if verbose:
            print(f"\n  {target['name']}: {vera_line}")

        if state.early_exit:
            if verbose:
                print(f"\n  [Vera ended conversation early: {state.early_exit_reason}]")
            break

        # --- Suitor responds ---
        is_last = (i == exchanges - 2)
        suitor_reply_prompt = (
            f"{target['name']} just said:\n"
            f'"{vera_line}"\n\n'
            f"Respond naturally. Be yourself."
            + (" This is your last exchange." if is_last else "")
        )
        suitor_messages_reply = [{"role": "user", "content": suitor_reply_prompt}]

        try:
            suitor_line, _ = run_agent_loop(
                system=suitor_system,
                messages=suitor_messages_reply,
                tools=SUITOR_TOOLS,
                tool_executor=suitor_executor.execute,
                max_tool_calls=2,
                cacheable=True,
            )
        except AgentLoopError:
            suitor_line = call_llm(suitor_system, suitor_reply_prompt, model=MODEL)

        prev_suitor_line = suitor_line
        suitor_turn: dict[str, Any] = {"speaker": suitor["name"], "text": suitor_line}
        if annotate:
            suitor_turn["analysis"] = annotate_exchange(suitor, target, suitor_line)
        conversation.append(suitor_turn)
        state.exchange_count += 1

        if verbose:
            print(f"\n  {suitor['name']}: {suitor_line}")

    return conversation, state


# ---------------------------------------------------------------------------
# Vera's final ranking (agentic)
# ---------------------------------------------------------------------------

def _agentic_target_ranking(
    target: dict[str, Any],
    suitors: list[dict[str, Any]],
    sim_state: SimulationState,
    verbose: bool = False,
) -> tuple[str, dict[str, Any] | None]:
    """
    Vera ranks all suitors based on the full evening's memory.
    Uses Sonnet — this is a user-visible decision with narrative weight.
    Vera's memory contains all encounter summaries.
    """
    from src.prompts.agent_system import build_agent_prompt

    system = build_agent_prompt(target)

    # Embed the full evening memory
    memory_block = ""
    if sim_state.vera_memory:
        memory_block = "YOUR EVENING SO FAR:\n"
        for i, mem in enumerate(sim_state.vera_memory, 1):
            memory_block += f"\n[Encounter {i}]\n{mem}\n"

    prompt = (
        f"{memory_block}\n"
        f"The evening is over. Rank all {len(suitors)} men from most to least interesting "
        f"as a potential second date, based entirely on how each conversation actually felt.\n\n"
        f"For each, give a 1-sentence gut reaction.\n\n"
        f"You may also say 'none of them' if nobody stood out enough for a second date.\n\n"
        f"Format:\n"
        + "\n".join(f"{i+1}. Name - reaction" for i in range(len(suitors)))
        + "\n\nIf you want to see none of them, put 'None' as the name for rank 1, "
        "then list the men in order of how close they came."
    )

    ranking_text = call_llm(system, prompt, model=MODEL, cacheable=True)

    if verbose:
        print(f"\n{'='*60}")
        print(f"  {target['name']}'s Final Rankings")
        print(f"{'='*60}")
        print(ranking_text)

    # Parse chosen from first ranked line
    chosen: dict[str, Any] | None = suitors[0]
    for line in ranking_text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if line_stripped.lower().startswith("1.") and "none" in line_stripped.lower():
            chosen = None
            break
        for suitor in suitors:
            if suitor["name"] in line_stripped and line_stripped.startswith("1."):
                chosen = suitor
                break
        else:
            continue
        break

    if verbose:
        if chosen:
            print(f"\n  >> {target['name']} wants to see {chosen['name']} again.")
        else:
            print(f"\n  >> {target['name']} chose nobody for a second date.")

    return ranking_text, chosen


# ---------------------------------------------------------------------------
# Main agentic bar-night entry point
# ---------------------------------------------------------------------------

def run_agentic_bar_night(
    target: dict[str, Any],
    suitors: list[dict[str, Any]],
    verbose: bool = True,
    annotate: bool = False,
) -> dict[str, Any]:
    """
    Run the full bar-night simulation in agentic mode.

    Returns the same dict shape as run_bar_night() in dynamics.py so that
    main.py's build_enriched_bar_night(), save_results(), and write_viewer_data()
    work without any modifications.

    Required output keys:
      target, suitors, encounters, ranking_text, chosen,
      compatibility, svr, gottman, evaluation
    """
    total = len(suitors)

    print(f"\n{'#'*60}")
    print(f"  BAR NIGHT (AGENTIC) — {target['name']} ({target['archetype']})")
    print(f"  {total} suitors, agentic mode — dual model + prompt caching")
    print(f"{'#'*60}")

    sim_state = SimulationState()
    encounters: list[dict[str, Any]] = []

    # -----------------------------------------------------------------------
    # Tier A+B: Orchestrator sequences encounters, suitors and Vera run agentic
    # -----------------------------------------------------------------------

    # Build orchestrator state for event decisions
    orch_system = build_orchestrator_prompt(target, suitors)

    def _evaluator_callback(chosen_suitor_id: str) -> dict[str, Any]:
        """Injected into OrchestratorToolExecutor to call evaluate_match()."""
        chosen = next((s for s in suitors if s["id"] == chosen_suitor_id), None)
        if chosen is None:
            return {"error": f"No suitor with id {chosen_suitor_id}"}
        chosen_convo = next(
            (e["conversation"] for e in encounters if e["suitor"]["id"] == chosen_suitor_id),
            [],
        )
        compat = compute_compatibility(target, chosen)
        evaluation = evaluate_match(target, chosen, chosen_convo, compat, verbose=False)
        return {"evaluation": evaluation}

    orch_executor = OrchestratorToolExecutor(
        sim_state=sim_state,
        target=target,
        all_suitors=suitors,
        evaluator_callback=_evaluator_callback,
    )

    for i, suitor in enumerate(suitors):
        fatigue = i / max(total - 1, 1)
        fatigue_label = (
            "fresh" if fatigue <= 0.25 else
            "mildly tired" if fatigue <= 0.50 else
            "fatigued" if fatigue <= 0.75 else
            "exhausted"
        )

        # --- Orchestrator decides whether to inject an event (Haiku) ---
        if i > 0:  # No event before the very first encounter
            orch_prompt = (
                f"Encounter {i+1} of {total} is about to begin. "
                f"Suitor: {suitor['name']} ({suitor['archetype']}, ID: {suitor['id']}). "
                f"Events used so far: {total - len(suitors) + i}. "
                f"Should you introduce an environmental event before this encounter? "
                f"Call introduce_event if yes, or produce a brief director's note if no event is needed."
            )
            orch_messages = [{"role": "user", "content": orch_prompt}]
            try:
                _, orch_messages = run_agent_loop(
                    system=orch_system,
                    messages=orch_messages,
                    tools=ORCHESTRATOR_TOOLS,
                    tool_executor=orch_executor.execute,
                    dialogue_model=MODEL_FAST,   # Haiku for sequencing decisions
                    reasoning_model=MODEL_FAST,
                    max_tool_calls=1,
                    cacheable=True,
                )
            except AgentLoopError:
                pass  # Non-critical — proceed without event

        print(f"\n{'-'*60}")
        print(f"  Encounter {i+1}/{total}: {suitor['name']} ({suitor['archetype']}) approaches")
        print(f"  Vera's fatigue: {fatigue:.2f} ({fatigue_label})")
        if sim_state.pending_events:
            print(f"  Active event: {sim_state.pending_events[0]}")
        print(f"{'-'*60}")

        # --- Run the agentic encounter ---
        conversation, conv_state = _run_agentic_encounter(
            suitor=suitor,
            target=target,
            sim_state=sim_state,
            convo_num=i + 1,
            total_suitors=total,
            exchanges=3,
            verbose=verbose,
            annotate=annotate,
        )

        # Add encounter to transcripts
        encounters.append({
            "suitor": suitor,
            "conversation": conversation,
            "fatigue_at_start": fatigue,
        })

        # Update Vera's memory with a plain-text summary of this encounter
        memory_entry = _summarize_encounter_for_memory(
            suitor=suitor,
            conversation=conversation,
            early_exit=conv_state.early_exit,
            early_exit_reason=conv_state.early_exit_reason,
        )
        sim_state.vera_memory.append(memory_entry)

    # -----------------------------------------------------------------------
    # Vera's final ranking
    # -----------------------------------------------------------------------
    ranking_text, chosen = _agentic_target_ranking(
        target=target,
        suitors=suitors,
        sim_state=sim_state,
        verbose=verbose,
    )

    # -----------------------------------------------------------------------
    # Tier C: Compatibility scoring + Gottman + Evaluation (if Vera chose someone)
    # -----------------------------------------------------------------------
    compat = svr = gottman = evaluation = None

    if chosen is not None:
        chosen_convo = next(
            e["conversation"] for e in encounters if e["suitor"]["id"] == chosen["id"]
        )
        compat = compute_compatibility(target, chosen)
        svr = svr_total(target, chosen)
        gottman = predict_gottman(target, chosen, compat)

        if verbose:
            print(f"\n{'='*60}")
            print(f"  Compatibility: {target['name']} × {chosen['name']}")
            print(f"{'='*60}")
            print(f"  Overall:    {compat['overall']*100:.0f}%")
            print(f"  Attachment: {compat['attachment_compat']*100:.0f}%")
            print(f"  Strategy:   {'Aligned' if compat['strategy_match'] == 1 else 'Mismatched'}")
            fh = gottman["four_horsemen"]
            print(f"  Stability:  {gottman['stability_score']:.0f}/100 — {gottman['prediction']}")

        # --- Orchestrator calls evaluator via tool (Sonnet — narrative output) ---
        orch_final_prompt = (
            f"The evening is complete. {target['name']} chose {chosen['name']} (ID: {chosen['id']}). "
            f"Call call_evaluator with the chosen suitor's ID, then write your director's note."
        )
        orch_final_messages = [{"role": "user", "content": orch_final_prompt}]
        eval_result: dict[str, Any] = {}

        try:
            _, orch_final_messages = run_agent_loop(
                system=orch_system,
                messages=orch_final_messages,
                tools=ORCHESTRATOR_TOOLS,
                tool_executor=orch_executor.execute,
                dialogue_model=MODEL,         # Sonnet — director's note is narrative
                reasoning_model=MODEL_FAST,
                max_tool_calls=1,
                cacheable=True,
            )
            # Extract evaluator result from tool results in message history
            for msg in orch_final_messages:
                if msg.get("role") == "user":
                    for block in (msg.get("content") or []):
                        if isinstance(block, dict) and block.get("type") == "tool_result":
                            try:
                                eval_result = json.loads(block["content"])
                            except Exception:
                                pass
        except AgentLoopError:
            # Fallback: call evaluator directly
            eval_result = _evaluator_callback(chosen["id"])

        evaluation = eval_result.get("evaluation") or evaluate_match(
            target, chosen, chosen_convo, compat, verbose
        )

        if verbose:
            print(f"\n{'='*60}")
            print("  Relationship Evaluator")
            print(f"{'='*60}")
            print(evaluation)

    return {
        "target": target,
        "suitors": suitors,
        "encounters": encounters,
        "ranking_text": ranking_text,
        "chosen": chosen,
        "compatibility": compat,
        "svr": svr,
        "gottman": gottman,
        "evaluation": evaluation,
    }
