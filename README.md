# Dating Game Agent Simulation

## Abstract

This project implements a computational agent-based model (ABM) of human mate selection in a simulated speed-dating context. Six agents — one target and five suitors — are parameterized on the Big Five personality dimensions (Costa & McCrae, 1992), adult attachment styles (Hazan & Shaver, 1987; Bartholomew & Horowitz, 1991), and mating strategies (Buss & Schmitt, 1993). Compatibility scoring is performed by a rule-based engine grounded in Murstein's (1970) Stimulus-Value-Role theory, assortative mating research (Thiessen & Gregg, 1980), and Gottman's Four Horsemen framework (Gottman et al., 1998). A large language model (LLM) serves as a dialogue engine: it translates each agent's psychological parameters into natural language exchanges. In the agentic operating mode, agents are additionally equipped with tool-use capabilities — they can query their own compatibility scores, shift strategy, and read engagement signals mid-conversation — giving ABM actors bounded autonomy without replacing the rule-based scoring layer. The system operates in two modes: a scripted mode in which Python controls all flow (LLMs generate text only), and an agentic mode in which an orchestrator agent manages encounter sequencing and each participant is an autonomous LLM agent. Both modes produce quantified compatibility scores, Gottman stability predictions, and a narrative evaluator verdict for each pairing.

---

## Research Question

**Can LLM agents simulate empirically grounded mate selection dynamics?**

This project is situated in the computational social science tradition of agent-based modeling (ABM). Three design commitments follow from that framing:

1. **LLM as dialogue engine, not autonomous reasoner.** Each agent's conversational behavior is mechanically derived from its Big Five scores and attachment style via explicit behavioral rules in the system prompt. The LLM does not determine compatibility outcomes — that is handled entirely by Python functions grounded in published empirical weights.

2. **Scoring functions as scientific claims.** Every weight, threshold, and formula in `compatibility.py` and `selection.py` is justified by a specific citation. The Gottman 5:1 ratio is 5:1 because the research says so. The attachment compatibility matrix values are derived from Hazan & Shaver (1987) and Kirkpatrick & Davis (1994). No parameter was tuned to produce desired outcomes.

3. **Agentic upgrade as bounded autonomy.** The agentic mode adds tool-use so ABM actors can query their own scoring functions. This gives agents bounded autonomy — they can read signals and adapt strategy — but they cannot modify the underlying scoring math. The scoring modules (`compatibility.py`, `selection.py`) are frozen and called as tools, not rewritten.

---

## Theoretical Framework

Every mechanic in this system is traceable to a specific paper. The table below documents the full theoretical stack; detailed operationalization follows.

| Theory | Paper | What we use | File |
|--------|-------|-------------|------|
| Five-Factor Model (Big Five) | Costa & McCrae (1992) | Personality parameterization; drives behavioral rules in system prompts | `personas.json`, `agent_system.py` |
| Adult Attachment Theory | Bowlby (1969); Hazan & Shaver (1987); Bartholomew & Horowitz (1991) | Four-style taxonomy; empirical compatibility matrix values | `compatibility.py`, `agent_system.py` |
| Stimulus-Value-Role Theory | Murstein (1970) | Three-stage selection engine; stage weights (S=0.30, V=0.40, R=0.30) | `selection.py` |
| Necessities vs. Luxuries | Li et al. (2002) | Budget model separating necessity traits from luxury traits | `selection.py` |
| Assortative Mating | Thiessen & Gregg (1980) | Cosine similarity for Big Five and trait vectors | `compatibility.py` |
| Four Horsemen + 5:1 Ratio | Gottman et al. (1998); Gottman (1994) | Trait-derived Horsemen proxies; stability prediction with 5:1 threshold | `compatibility.py` |
| Predictive conversation window | Carrere & Gottman (1999) | Grounds 3-exchange speed date as a predictive window for relational dynamics | `dynamics.py` |
| Sexual Strategies Theory | Buss & Schmitt (1993) | Strategy alignment penalty (mismatch cost = 0.4 on role-fit dimension) | `compatibility.py`, `selection.py` |

### Personality Architecture: Big Five (NEO-PI-R)

Agents are profiled on the five-factor model as operationalized by Costa & McCrae (1992). Each trait is a continuous value in [0, 100] and directly drives both conversational behavior and compatibility scoring:

| Trait | Behavioral Effect in Simulation |
|-------|--------------------------------|
| Openness | Abstract language, metaphor use, creative tangents vs. concrete and practical |
| Conscientiousness | Planning orientation vs. spontaneity; role-fit scoring in SVR Stage 3 |
| Extraversion | Response length, initiation rate, silence tolerance |
| Agreeableness | Conflict avoidance vs. directness; Four Horsemen risk amplifier |
| Neuroticism | Hedging, second-guessing, validation-seeking; Four Horsemen amplifier |

### Attachment Theory

Each agent carries one of four attachment styles derived from Bartholomew & Horowitz's (1991) four-category model. Hazan & Shaver (1987) originally identified three adult styles (secure, anxious-ambivalent, avoidant); Bartholomew & Horowitz (1991) added fearful-avoidant, characterized by simultaneous desire for and fear of closeness, producing approach-then-retreat behavior. Compatibility scores are drawn from an empirical matrix based on Hazan & Shaver (1987) and Kirkpatrick & Davis (1994):

| Style | Conversational Signature | Example |
|-------|--------------------------|---------|
| Secure | Balanced disclosure; comfortable with silence | Marcus |
| Anxious-preoccupied | Seeks validation; reads into neutral signals; escalates quickly | Theo, Rafael |
| Dismissive-avoidant | Intellectualizes emotion; deflects personal questions | Elliot |
| Fearful-avoidant | Approach-then-retreat; hot-cold oscillation | Dex |

The anxious + avoidant pairing receives the lowest compatibility score (0.25) — the "classic trap" identified extensively in the attachment literature (Kirkpatrick & Davis, 1994).

### Mate Selection: Stimulus-Value-Role Theory

The selection engine implements Murstein's (1970) three-stage courtship model:

- **Stage 1 — Stimulus (weight: 0.30):** Initial attraction from observable traits — physical attractiveness, humor, extraversion. Corresponds to first-impression processing.
- **Stage 2 — Value (weight: 0.40):** Deep compatibility on personality and values, measured via Big Five cosine similarity. Weighted highest as the strongest predictor of long-term relationship success per Murstein (1970).
- **Stage 3 — Role (weight: 0.30):** Functional fit in relationship roles — mating strategy alignment and conscientiousness complementarity.

### Necessities vs. Luxuries

The selection engine distinguishes necessity traits (kindness, intelligence, stability) from luxury traits (attractiveness, status, humor) following Li et al. (2002). Necessities function as minimum thresholds evaluated before luxury traits.

> **Adaptation note:** Li et al.'s original findings were sex-differentiated — attractiveness was a necessity for men, resources for women. This simulation uses a sex-averaged version. The inclusion of *stability* as a necessity draws on Gottman's stability literature rather than Li et al. directly.

### Compatibility Scoring

The full compatibility score is a weighted composite across four dimensions:

| Dimension | Weight | Justification |
|-----------|--------|---------------|
| Attachment compatibility | 0.35 | Strongest single predictor (Hazan & Shaver, 1987) |
| Big Five similarity | 0.25 | Assortative mating: moderate predictor (Thiessen & Gregg, 1980) |
| Trait similarity | 0.20 | Secondary to attachment (Li et al., 2002) |
| Strategy alignment | 0.20 | Mismatch is a dealbreaker (Buss & Schmitt, 1993) |

Big Five and trait similarity are computed via cosine similarity, operationalizing the assortative mating literature (Thiessen & Gregg, 1980).

### Relationship Stability: Gottman's Four Horsemen

Stability prediction uses Gottman's Four Horsemen framework. Each Horseman is computed as a trait-derived proxy from Big Five scores and attachment style, rather than through observational coding of live conversation (Gottman's original method used the Specific Affect Coding System, SPAFF):

| Horseman | Trait-Derived Proxy |
|----------|---------------------|
| Criticism | f(neuroticism × low agreeableness) |
| Contempt | f(low attachment compatibility, neuroticism) |
| Defensiveness | f(neuroticism, low agreeableness) |
| Stonewalling | f(low stability, avoidant attachment) |

The **5:1 positive-to-negative interaction ratio** (Gottman, 1994) is computed as a proxy using agreeableness, stability, and overall compatibility. Couples below 5:1 are classified as "at risk"; those below 1:1 as "likely to dissolve." Stability scores are reported on a 0–100 scale with explicit thresholds.

Carrere & Gottman (1999) demonstrated that divorce can be predicted from as little as the first three minutes of a couple's conflict discussion — providing theoretical grounding for using brief 3-exchange speed-date conversations as predictive windows into relational dynamics.

### Sexual Strategies Theory

Agents carry a declared mating strategy (long-term or short-term). Strategy mismatch is modeled as a high-cost penalty (role-fit contribution of 0.4 vs. 1.0) on the premise that conflicting reproductive strategies predict relational instability (Buss & Schmitt, 1993).

---

## System Architecture

The simulation operates in two distinct modes: a **scripted mode** in which Python controls all flow, and an **agentic mode** in which each participant is an autonomous LLM agent with tool access.

### Scripted Mode (`python src/main.py`)

Python drives the entire simulation loop. LLMs generate dialogue text only; all scoring is post-hoc rule-based computation.

```
Each suitor approaches in sequence
         │
         ▼
Speed date: 3-exchange conversation (LLM × LLM)
  - Suitor: Big Five + attachment behavioral rules → natural language
  - Vera:   same, plus fatigue state (0.0–1.0) injected into system prompt
         │
         ▼
Target ranks all suitors (LLM, sees full transcript)
         │
         ▼
Compatibility engine (rule-based, runs once on chosen pair)
  ├── Attachment compatibility matrix     [Hazan & Shaver]
  ├── Big Five cosine similarity          [assortative mating]
  ├── Trait vector cosine similarity      [Li et al.]
  └── Strategy alignment penalty          [Buss & Schmitt]
         │
         ▼
Gottman evaluator (rule-based)
  ├── Four Horsemen risk scores
  ├── Positive/negative ratio (5:1 threshold)
  └── Stability score (0–100) + prediction
         │
         ▼
Relationship psychologist agent (LLM)
  ├── Reads conversation + all computed metrics
  ├── Cites psychological mechanisms by name
  └── Delivers 4–6 sentence structured verdict
```

### Agentic Mode (`python src/main.py --agentic`)

An orchestrator agent replaces the Python loop. Scoring modules become tools agents query mid-conversation. Each participant has bounded autonomy.

```
Orchestrator agent (Haiku)
  ├── Sequences encounters
  └── Optionally calls introduce_event() before each encounter
         │
         ▼  (per suitor)
Suitor agent loop (Sonnet for dialogue, Haiku for tool turns)
  ├── Tool: check_compatibility(target_id)
  │         → calls compute_compatibility() + svr_total() [frozen]
  ├── Tool: change_strategy(new_strategy)
  │         → mutates session-only strategy label
  ├── Tool: read_body_language()
  │         → word-list sentiment on Vera's last message (no API call)
  └── Spoken dialogue line → Vera's context
         │
         ▼
Vera agent loop (Sonnet)
  ├── Persistent memory: all prior encounter transcripts in system prompt
  ├── Tool: end_conversation_early(reason)
  │         → sets early_exit flag; orchestrator breaks encounter loop
  └── Spoken dialogue line → suitor's context
         │
         ▼  (after all encounters)
Vera final ranking (Sonnet, sees full evening memory)
         │
         ▼
Orchestrator calls call_evaluator(chosen_suitor_id)
  → compute_compatibility() + predict_gottman() + evaluate_match() [frozen]
```

**Cost optimizations in agentic mode:**
- Dual-model strategy: Sonnet for turn-start calls (dialogue); Haiku for tool-continuation calls (reasoning after tool results)
- `max_tool_calls=2` cap per encounter with forced `end_turn` on overflow
- Prompt caching (`cache_control: ephemeral`) on all agent system prompts — ~90% input token discount on repeated calls
- Annotation is opt-in only (`--annotate` flag)

### Module Map

```
dating_game/
├── src/
│   ├── agents/
│   │   ├── personas.json              ← Big Five profiles, attachment styles, traits
│   │   ├── agent_loop.py              ← Universal agentic loop (dual-model, tool cap, caching)
│   │   ├── conversation_state.py      ← Per-encounter and full-run state containers
│   │   ├── tool_definitions.py        ← Anthropic tool schemas (suitor / target / orchestrator)
│   │   └── tool_executors.py          ← Execution layer (wraps frozen scoring modules as tools)
│   ├── models/
│   │   ├── compatibility.py           ← Attachment matrix, Gottman scoring [FROZEN]
│   │   ├── selection.py               ← SVR theory, necessity/luxury model [FROZEN]
│   │   └── dynamics.py                ← Scripted simulation flow
│   ├── prompts/
│   │   ├── agent_system.py            ← Builds agent system prompts from Big Five profiles
│   │   ├── evaluator_system.py        ← Relationship psychologist prompt
│   │   ├── annotation_system.py       ← Per-exchange behavioral annotator prompt
│   │   └── orchestrator_system.py     ← Agentic suitor/target/orchestrator prompt builders
│   ├── utils/
│   │   └── llm_client.py              ← Shared Anthropic client; call_llm with caching support
│   ├── agentic_main.py                ← run_agentic_bar_night() — three-tier agentic loop
│   └── main.py                        ← Entry point; CLI flag handling
├── viewer/
│   ├── index.html                     ← Browser-based simulation viewer
│   └── data.js                        ← Last simulation result (written by --serve)
└── output/                            ← JSON simulation results (gitignored)
```

---

## Agent Profiles

One target (Vera) and five suitors. Big Five scores are on a 0–100 scale. All profiles are defined in `src/agents/personas.json`.

| Agent | Role | O | C | E | A | N | Attachment | Strategy | Archetype |
|-------|------|---|---|---|---|---|------------|----------|-----------|
| Vera | Target | 85 | 78 | 70 | 62 | 42 | Secure | Long-term | Curator |
| Marcus | Suitor | 72 | 82 | 65 | 75 | 28 | Secure | Long-term | Architect |
| Theo | Suitor | 78 | 48 | 92 | 70 | 78 | Anxious-preoccupied | Short-term | Performer |
| Elliot | Suitor | 90 | 75 | 32 | 42 | 35 | Dismissive-avoidant | Long-term | Analyst |
| Rafael | Suitor | 82 | 52 | 74 | 82 | 72 | Anxious-preoccupied | Long-term | Romantic |
| Dex | Suitor | 88 | 38 | 60 | 58 | 68 | Fearful-avoidant | Short-term | Drifter |

*O = Openness, C = Conscientiousness, E = Extraversion, A = Agreeableness, N = Neuroticism*

### Predicted Pairings of Interest

| Pairing | Predicted Dynamic | Theoretical Basis |
|---------|------------------|-------------------|
| Vera × Marcus | Highest predicted stability | Secure + secure; matched strategy; Big Five value alignment |
| Vera × Elliot | Intellectual rapport; low warmth | Dismissive-avoidant + secure; high O similarity; low A on Elliot's side |
| Vera × Theo | Initial chemistry, structural collapse | Anxious + secure; strategy mismatch (short vs. long-term); N=78 instability |
| Vera × Rafael | Sincere but suffocating | Anxious + secure; A=82 overcommunication meets someone who "spots rehearsed lines" |
| Vera × Dex | Magnetic then withdrawn | Fearful-avoidant approach-retreat vs. secure consistency; C=38 instability |

---

## Cost Analysis

API call estimates assume average exchange length of ~800 input tokens and ~200 output tokens per call. Prompt caching assumes ~90% of input tokens are cache hits after the first call in each encounter.

| Mode | Models | API calls/run | Est. cost/run | Notes |
|------|--------|--------------|---------------|-------|
| Scripted | Sonnet only | 17 | ~$0.09 | 15 dialogue + 1 ranking + 1 evaluator |
| Scripted + `--annotate` | Sonnet only | 32 | ~$0.16 | +15 per-exchange annotation calls |
| Agentic (naive, all Sonnet, no cache) | Sonnet only | ~50 | ~$0.60 | Baseline agentic without optimizations |
| **Agentic (dual-model + prompt cache)** | Sonnet + Haiku | ~50 | **~$0.17** | Sonnet for dialogue; Haiku for tool turns; prompt caching |
| Agentic + `--annotate` | Sonnet + Haiku | ~65 | ~$0.19 | +15 Haiku annotation calls |

Pricing (as of April 2026): Haiku — $0.80/$4.00 per million input/output tokens; cache read $0.08/M. Sonnet — $3.00/$15.00 per million input/output tokens; cache read $0.30/M. The dual-model and caching optimizations recover approximately 70% of the raw cost increase from scripted to agentic mode.

---

## Setup

### Prerequisites

- Python 3.9+
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

### Install

```bash
pip install anthropic
```

### Configure

Create `config.py` in the project root (this file is gitignored and must never be committed):

```python
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
MODEL = "claude-sonnet-4-20250514"
MODEL_FAST = "claude-haiku-4-5-20251001"
```

### Run

```bash
# Scripted mode (default)
py -3.9 src/main.py

# Scripted mode, minimal output
py -3.9 src/main.py --quiet

# Scripted + per-exchange psychological annotations
py -3.9 src/main.py --annotate

# Annotated run + open browser viewer
py -3.9 src/main.py --serve

# Full agentic mode (tool-using agents, dual-model, prompt caching)
py -3.9 src/main.py --agentic

# Agentic, minimal output
py -3.9 src/main.py --agentic --quiet

# Agentic + per-exchange annotations
py -3.9 src/main.py --agentic --annotate
```

### CLI Flags

| Flag | Effect | Cost impact |
|------|--------|-------------|
| *(none)* | Scripted mode, verbose console output | Baseline (~$0.09) |
| `--quiet` | Scripted mode, minimal output | Same as above |
| `--annotate` | Add per-exchange LLM behavioral annotation to each conversation turn | +$0.07 |
| `--serve` | Run annotated simulation and open viewer in browser (implies `--annotate`) | +$0.07 |
| `--agentic` | Agentic mode: tool-using agents, orchestrator, dual-model, prompt caching | ~$0.17 |
| `--agentic --annotate` | Agentic mode with per-exchange annotations | ~$0.19 |

---

## Output Format

Each run writes a timestamped JSON file to `output/` (gitignored). The `--serve` flag additionally writes `viewer/data.js` for the browser viewer.

```json
{
  "meta": {
    "timestamp": "2026-04-01T01:24:36",
    "model": "claude-sonnet-4-20250514",
    "scenario": "bar_night"
  },
  "target": { "id": "T", "name": "Vera", ... },
  "suitors": [ ... ],
  "encounters": [
    {
      "suitor": { "id": "S1", "name": "Marcus", ... },
      "conversation": [
        { "speaker": "Marcus", "text": "...", "analysis": { ... } }
      ],
      "fatigue_at_start": 0.0
    }
  ],
  "rankings": [
    { "rank": 1, "name": "Marcus", "reaction": "..." }
  ],
  "chosen": { "id": "S1", "name": "Marcus", ... },
  "compatibility": {
    "big5_similarity": 0.872,
    "trait_similarity": 0.801,
    "attachment_compat": 0.950,
    "strategy_match": 1.0,
    "overall": 0.893
  },
  "gottman": {
    "four_horsemen": {
      "criticism": 0.12, "contempt": 0.08,
      "defensiveness": 0.14, "stonewalling": 0.09
    },
    "positive_negative_ratio": 7.4,
    "stability_score": 84.2,
    "prediction": "Likely stable"
  },
  "evaluation": "..."
}
```

---

## Limitations and Future Work

### Current Limitations

1. **Four Horsemen are trait-derived proxies.** Gottman's original research used the Specific Affect Coding System (SPAFF) to code observed behavior in live marital conflict discussions. This simulation derives Horsemen scores from static personality traits — a modeling simplification that collapses within-person variability and situational context.

2. **`read_body_language()` uses a word-list heuristic.** Engagement scoring in the agentic mode is a bag-of-words approximation (LIWC-inspired positive/negative word lists). No syntactic, pragmatic, or prosodic analysis is performed.

3. **Binary mating strategies.** Real mating strategies exist on a continuum; the long-term/short-term dichotomy is a simplification of Sexual Strategies Theory, which treats strategic flexibility as a key feature (Buss & Schmitt, 1993).

4. **No longitudinal dynamics.** Gottman's predictive research is primarily longitudinal — newlywed studies tracked over 6 years. This simulation models a single evening; accumulated relational behavior over time is not represented.

5. **Memory as serialized text.** Vera's cross-encounter memory is embedded as plain text in her system prompt. There is no vector retrieval, episodic weighting, or recency bias — all prior encounters are equally salient.

6. **Fixed agent pool.** The simulation always runs with the same five suitors. Agent count and composition are not parameterized.

### Future Work

- **Conversation-based Horsemen scoring.** Replace trait-derived proxies with LLM-based SPAFF approximation on the actual conversation transcript.
- **Multi-round longitudinal simulation.** Track compatibility and stability scores across repeated encounters to model relationship development over time.
- **Variable agent pools.** Parameterize agent count, sex ratios, and personality distributions to enable population-level analysis.
- **Continuous strategy dimension.** Replace the binary long-term/short-term flag with a continuous strategic orientation score per Gangestad & Simpson (2000).
- **Vera's fatigue as a dynamic variable.** Currently computed deterministically from encounter order; could be modeled as a function of actual conversation quality.

---

## References

Bartholomew, K., & Horowitz, L. M. (1991). Attachment styles among young adults: A test of a four-category model. *Journal of Personality and Social Psychology, 61*(2), 226–244. https://doi.org/10.1037/0022-3514.61.2.226

Bowlby, J. (1969). *Attachment and Loss, Vol. 1: Attachment*. Basic Books.

Buss, D. M., & Schmitt, D. P. (1993). Sexual strategies theory: An evolutionary perspective on human mating. *Psychological Review, 100*(2), 204–232. https://doi.org/10.1037/0033-295X.100.2.204

Carrere, S., & Gottman, J. M. (1999). Predicting divorce among newlyweds from the first three minutes of a marital conflict discussion. *Family Process, 38*(3), 293–301. https://doi.org/10.1111/j.1545-5300.1999.00293.x

Costa, P. T., & McCrae, R. R. (1992). *Revised NEO Personality Inventory (NEO-PI-R) and NEO Five-Factor Inventory (NEO-FFI) professional manual*. Psychological Assessment Resources.

Gangestad, S. W., & Simpson, J. A. (2000). The evolution of human mating: Trade-offs and strategic pluralism. *Behavioral and Brain Sciences, 23*(4), 573–587.

Gottman, J. M. (1994). *What Predicts Divorce? The Relationship Between Marital Processes and Marital Outcomes*. Lawrence Erlbaum.

Gottman, J. M., Coan, J., Carrere, S., & Swanson, C. (1998). Predicting marital happiness and stability from newlywed interactions. *Journal of Marriage and Family, 60*(1), 5–22. https://doi.org/10.2307/353438

Hazan, C., & Shaver, P. (1987). Romantic love conceptualized as an attachment process. *Journal of Personality and Social Psychology, 52*(3), 511–524. https://doi.org/10.1037/0022-3514.52.3.511

Kirkpatrick, L. A., & Davis, K. E. (1994). Attachment style, gender, and relationship stability: A longitudinal analysis. *Journal of Personality and Social Psychology, 66*(3), 502–512. https://doi.org/10.1037/0022-3514.66.3.502

Li, N. P., Bailey, J. M., Kenrick, D. T., & Linsenmeier, J. A. W. (2002). The necessities and luxuries of mate preferences: Testing the tradeoffs. *Journal of Personality and Social Psychology, 82*(6), 947–955. https://doi.org/10.1037/0022-3514.82.6.947

Murstein, B. I. (1970). Stimulus-value-role: A theory of marital choice. *Journal of Marriage and the Family, 32*(3), 465–481. https://doi.org/10.2307/350113

Thiessen, D., & Gregg, B. (1980). Human assortative mating and genetic equilibrium: An evolutionary perspective. *Ethology and Sociobiology, 1*(2), 111–140. https://doi.org/10.1016/0162-3095(80)90003-5
