"""
Simulation dynamics: the dating round engine.

Orchestrates the full flow:
1. Picker ranks candidates (LLM)
2. Speed date conversation (LLM × LLM)
3. Compatibility scoring (rule-based)
4. Gottman evaluation (rule-based)
5. Qualitative evaluation (LLM)
"""

from __future__ import annotations
import json
import os
from typing import Any

from src.prompts.agent_system import build_agent_prompt, build_target_prompt
from src.prompts.annotation_system import ANNOTATION_SYSTEM_PROMPT
from src.prompts.evaluator_system import EVALUATOR_SYSTEM_PROMPT
from src.models.compatibility import compute_compatibility, predict_gottman
from src.models.selection import svr_total
from src.utils.llm_client import call_llm, client  # noqa: F401  (client kept for compat)


def annotate_exchange(
    speaker: dict[str, Any],
    listener: dict[str, Any],
    text: str,
) -> dict[str, str]:
    """
    Generate a psychological annotation for a single conversation exchange.

    Returns a dict with keys: label, detail, theory.
    On any failure, returns a safe fallback so the simulation never crashes.
    """
    user_message = f"""SPEAKER: {speaker["name"]} ({speaker["archetype"]})
Big Five: O{speaker["big5"]["openness"]} C{speaker["big5"]["conscientiousness"]} E{speaker["big5"]["extraversion"]} A{speaker["big5"]["agreeableness"]} N{speaker["big5"]["neuroticism"]}
Attachment: {speaker["attachment"]} | Strategy: {speaker["strategy"]}

LISTENER: {listener["name"]} ({listener["archetype"]})
Big Five: O{listener["big5"]["openness"]} C{listener["big5"]["conscientiousness"]} E{listener["big5"]["extraversion"]} A{listener["big5"]["agreeableness"]} N{listener["big5"]["neuroticism"]}
Attachment: {listener["attachment"]} | Strategy: {listener["strategy"]}

EXCHANGE:
\"{text}\""""

    raw = call_llm(ANNOTATION_SYSTEM_PROMPT, user_message)

    # Strip markdown fences if the model wrapped the JSON anyway
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[-1] if cleaned.count("```") >= 2 else cleaned
        cleaned = cleaned.removeprefix("json").strip().rstrip("`").strip()

    try:
        parsed = json.loads(cleaned)
        if not {"label", "detail", "theory"}.issubset(parsed.keys()):
            raise ValueError("Missing required keys")
        return {"label": str(parsed["label"]), "detail": str(parsed["detail"]), "theory": str(parsed["theory"])}
    except Exception:
        return {"label": "Analysis unavailable", "detail": "[annotation failed]", "theory": ""}


def rank_candidates(
    picker: dict[str, Any],
    others: list[dict[str, Any]],
    verbose: bool = False,
) -> tuple[str, dict[str, Any]]:
    """
    Phase 1: Picker ranks the other candidates via LLM.
    Returns (ranking_text, top_pick_agent).
    """
    prompt = "You're at a speed dating event. Here are your 4 potential dates:\n\n"
    for o in others:
        prompt += f"{o['name']} ({o['archetype']}): {o['bio']}\n\n"
    prompt += (
        "Rank them from most to least appealing to you. "
        "For each, give a 1-sentence gut reaction. Format as:\n"
        "1. Name - reaction\n2. Name - reaction\n"
        "3. Name - reaction\n4. Name - reaction"
    )

    system = build_agent_prompt(picker)
    ranking_text = call_llm(system, prompt)

    if verbose:
        print(f"\n{'='*60}")
        print(f"  {picker['name']}'s Rankings")
        print(f"{'='*60}")
        print(ranking_text)

    # Extract top pick: first name that matches an agent
    top_pick = others[0]  # fallback
    for o in others:
        first_line = ranking_text.split("\n")[0] if ranking_text else ""
        if o["name"] in first_line:
            top_pick = o
            break

    return ranking_text, top_pick


def speed_date(
    picker: dict[str, Any],
    match: dict[str, Any],
    exchanges: int = 3,
    verbose: bool = False,
    annotate: bool = False,
    target_system: str | None = None,
) -> list[dict[str, Any]]:
    """
    Phase 2: Speed date conversation between picker and match.
    Returns list of {speaker, text} dicts.
    """
    convo: list[dict[str, str]] = []
    picker_system = build_agent_prompt(picker)
    match_system = target_system if target_system is not None else build_agent_prompt(match)

    if verbose:
        print(f"\n{'='*60}")
        print(f"  Speed Date: {picker['name']} × {match['name']}")
        print(f"{'='*60}")

    # Opener from picker
    opener_prompt = (
        f"You're on a 3-minute speed date with {match['name']} "
        f"({match['archetype']}). {match['bio']}\n\n"
        f"Start with an opening line. Be yourself."
    )
    opener = call_llm(picker_system, opener_prompt)
    convo.append({"speaker": picker["name"], "text": opener})
    if annotate:
        convo[-1]["analysis"] = annotate_exchange(picker, match, opener)
    if verbose:
        print(f"\n  {picker['name']}: {opener}")

    # Back-and-forth
    prev_text = opener
    prev_speaker = picker
    for i in range(exchanges - 1):
        # Alternate speakers
        current = match if prev_speaker == picker else picker
        other = picker if current == match else match
        current_system = match_system if current == match else picker_system

        reply_prompt = (
            f"Speed date with {other['name']} ({other['archetype']}). "
            f"They just said:\n\n\"{prev_text}\"\n\n"
            f"Respond naturally. Be yourself."
        )
        if i == exchanges - 2:
            reply_prompt += " This is your last chance to make an impression."

        reply = call_llm(current_system, reply_prompt)
        convo.append({"speaker": current["name"], "text": reply})
        if annotate:
            listener = picker if current == match else match
            convo[-1]["analysis"] = annotate_exchange(current, listener, reply)
        if verbose:
            print(f"\n  {current['name']}: {reply}")

        prev_text = reply
        prev_speaker = current

    return convo


def evaluate_match(
    picker: dict[str, Any],
    match: dict[str, Any],
    convo: list[dict[str, str]],
    compat: dict[str, float],
    verbose: bool = False,
) -> str:
    """
    Phase 5: LLM relationship psychologist evaluates the pair.
    """
    convo_text = "\n".join(f'{c["speaker"]}: "{c["text"]}"' for c in convo)

    eval_prompt = f"""Evaluate this couple:

PERSON 1: {picker["name"]} ({picker["archetype"]})
- Big Five: O{picker["big5"]["openness"]} C{picker["big5"]["conscientiousness"]} E{picker["big5"]["extraversion"]} A{picker["big5"]["agreeableness"]} N{picker["big5"]["neuroticism"]}
- Attachment: {picker["attachment"]}
- Strategy: {picker["strategy"]}
- Bio: {picker["bio"]}

PERSON 2: {match["name"]} ({match["archetype"]})
- Big Five: O{match["big5"]["openness"]} C{match["big5"]["conscientiousness"]} E{match["big5"]["extraversion"]} A{match["big5"]["agreeableness"]} N{match["big5"]["neuroticism"]}
- Attachment: {match["attachment"]}
- Strategy: {match["strategy"]}
- Bio: {match["bio"]}

THEIR SPEED DATE CONVERSATION:
{convo_text}

COMPATIBILITY METRICS:
- Big Five similarity: {compat["big5_similarity"]*100:.0f}%
- Trait similarity: {compat["trait_similarity"]*100:.0f}%
- Attachment compatibility: {compat["attachment_compat"]*100:.0f}%
- Strategy match: {"Aligned" if compat["strategy_match"] == 1 else "Mismatched"}
- Overall: {compat["overall"]*100:.0f}%

Give your professional evaluation."""

    evaluation = call_llm(EVALUATOR_SYSTEM_PROMPT, eval_prompt)

    if verbose:
        print(f"\n{'='*60}")
        print(f"  Relationship Evaluator")
        print(f"{'='*60}")
        print(evaluation)

    return evaluation


def run_round(
    picker: dict[str, Any],
    all_agents: list[dict[str, Any]],
    verbose: bool = True,
    annotate: bool = False,
) -> dict[str, Any]:
    """
    Run a complete dating round. Returns all results as a dict.
    """
    others = [a for a in all_agents if a["id"] != picker["id"]]

    print(f"\n{'#'*60}")
    print(f"  ROUND: {picker['name']} ({picker['archetype']}) is looking for a date")
    print(f"{'#'*60}")

    # Phase 1: Rank
    ranking_text, top_pick = rank_candidates(picker, others, verbose)

    print(f"\n  >> {picker['name']} picks {top_pick['name']} ({top_pick['archetype']})")

    # Phase 2: Speed date
    convo = speed_date(picker, top_pick, exchanges=3, verbose=verbose, annotate=annotate)

    # Phase 3: Compatibility
    compat = compute_compatibility(picker, top_pick)
    svr = svr_total(picker, top_pick)

    # Phase 4: Gottman
    gottman = predict_gottman(picker, top_pick, compat)

    if verbose:
        print(f"\n{'='*60}")
        print(f"  Compatibility Scores")
        print(f"{'='*60}")
        print(f"  Overall:    {compat['overall']*100:.0f}%")
        print(f"  Big Five:   {compat['big5_similarity']*100:.0f}%")
        print(f"  Traits:     {compat['trait_similarity']*100:.0f}%")
        print(f"  Attachment: {compat['attachment_compat']*100:.0f}%")
        print(f"  Strategy:   {'Aligned' if compat['strategy_match'] == 1 else 'Mismatched'}")
        print(f"\n  SVR Scores:")
        print(f"  Stimulus: {svr['stimulus']*100:.0f}% | Value: {svr['value']*100:.0f}% | Role: {svr['role']*100:.0f}%")
        print(f"\n{'='*60}")
        print(f"  Gottman Analysis")
        print(f"{'='*60}")
        fh = gottman["four_horsemen"]
        print(f"  Criticism:      {fh['criticism']*100:.0f}%")
        print(f"  Contempt:       {fh['contempt']*100:.0f}%")
        print(f"  Defensiveness:  {fh['defensiveness']*100:.0f}%")
        print(f"  Stonewalling:   {fh['stonewalling']*100:.0f}%")
        print(f"  +/- Ratio:      {gottman['positive_negative_ratio']:.1f}:1 {'(healthy)' if gottman['positive_negative_ratio'] >= 5 else '(below 5:1)'}")
        print(f"  Stability:      {gottman['stability_score']:.0f}/100")
        print(f"  Prediction:     {gottman['prediction']}")

    # Phase 5: LLM evaluation
    evaluation = evaluate_match(picker, top_pick, convo, compat, verbose)

    return {
        "picker": picker["name"],
        "match": top_pick["name"],
        "ranking": ranking_text,
        "conversation": convo,
        "compatibility": compat,
        "svr": svr,
        "gottman": gottman,
        "evaluation": evaluation,
    }


def target_ranks(
    target: dict[str, Any],
    suitors: list[dict[str, Any]],
    conversations: list[list[dict[str, Any]]],
    verbose: bool = False,
) -> tuple[str, dict[str, Any] | None]:
    """
    After all encounters, the target ranks all suitors based on the actual conversations.

    Returns (ranking_text, chosen_suitor_or_None).
    If the target says "None" as her first choice, chosen is None.
    """
    system = build_agent_prompt(target)

    # Build transcript of all conversations
    convo_block = ""
    for i, (suitor, convo) in enumerate(zip(suitors, conversations)):
        convo_block += f"\nCONVERSATION {i+1} — {suitor['name']} ({suitor['archetype']}):\n"
        for ex in convo:
            convo_block += f'  {ex["speaker"]}: "{ex["text"]}"\n'

    prompt = (
        f"You just spent the evening at a bar having brief conversations with {len(suitors)} men. "
        f"Here is what happened:\n{convo_block}\n"
        f"Now rank all {len(suitors)} men from most to least interesting as a potential second date, "
        f"based entirely on how each conversation actually felt — not their appearance or reputation.\n"
        f"For each, give a 1-sentence gut reaction.\n\n"
        f"You may also say 'none of them' if nobody stood out enough for a second date.\n\n"
        f"Format:\n"
        + "\n".join(f"{i+1}. Name - reaction" for i in range(len(suitors)))
        + f"\n\nIf you want to see none of them, put 'None' as the name for rank 1, "
        f"then list the men in order of how close they came."
    )

    ranking_text = call_llm(system, prompt)

    if verbose:
        print(f"\n{'='*60}")
        print(f"  {target['name']}'s Final Rankings")
        print(f"{'='*60}")
        print(ranking_text)

    # Parse chosen: scan the first ranked line for a suitor name or "none"
    chosen: dict[str, Any] | None = suitors[0]  # fallback
    for line in ranking_text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        # Check for "none" first
        if line_stripped.lower().startswith("1.") and "none" in line_stripped.lower():
            chosen = None
            break
        # Check for a suitor name
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


def run_bar_night(
    target: dict[str, Any],
    suitors: list[dict[str, Any]],
    verbose: bool = True,
    annotate: bool = False,
) -> dict[str, Any]:
    """
    Run the full bar-night simulation.

    Flow: each suitor approaches the target in turn (with fatigue accumulating),
    then the target ranks all suitors and optionally selects one for a second date.
    Compatibility and Gottman scoring only run if the target chooses someone.
    """
    total = len(suitors)

    print(f"\n{'#'*60}")
    print(f"  BAR NIGHT — {target['name']} ({target['archetype']}) is being approached")
    print(f"  {total} suitors, conversations 1–{total}")
    print(f"{'#'*60}")

    encounters: list[dict[str, Any]] = []
    all_conversations: list[list[dict[str, Any]]] = []

    for i, suitor in enumerate(suitors):
        fatigue = i / (total - 1) if total > 1 else 0.0
        fatigue_label = (
            "fresh" if fatigue <= 0.25 else
            "mildly tired" if fatigue <= 0.50 else
            "fatigued" if fatigue <= 0.75 else
            "exhausted"
        )

        print(f"\n{'-'*60}")
        print(f"  Encounter {i+1}/{total}: {suitor['name']} ({suitor['archetype']}) approaches")
        print(f"  Vera's fatigue: {fatigue:.2f} ({fatigue_label})")
        print(f"{'-'*60}")

        target_sys = build_target_prompt(
            target, fatigue, convo_num=i + 1, total_suitors=total
        )
        convo = speed_date(
            picker=suitor,
            match=target,
            exchanges=3,
            verbose=verbose,
            annotate=annotate,
            target_system=target_sys,
        )

        encounters.append({
            "suitor": suitor,
            "conversation": convo,
            "fatigue_at_start": fatigue,
        })
        all_conversations.append(convo)

    # Target ranks all suitors based on full conversation history
    ranking_text, chosen = target_ranks(target, suitors, all_conversations, verbose)

    # Scoring and evaluation — only if a suitor was chosen
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

        evaluation = evaluate_match(target, chosen, chosen_convo, compat, verbose)

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
