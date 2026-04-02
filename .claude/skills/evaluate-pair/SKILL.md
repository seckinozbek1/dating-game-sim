---
name: evaluate-pair
description: Evaluate compatibility between two specific agents without running a full simulation. Use when user says "how would X and Y work together", "evaluate", "score this pair", or "what about X and Y".
argument-hint: "[agent1_name] [agent2_name]"
---

# Evaluate Pair

## Steps
1. Load both agents from personas.json
2. Compute compatibility scores (Big Five sim, trait sim, attachment, strategy)
3. Run Gottman scoring (Four Horsemen, ratio, stability)
4. Call the LLM evaluator for a qualitative assessment
5. Print a structured report:
   - Overall compatibility %
   - Each sub-score with explanation
   - Four Horsemen risk levels
   - Stability prediction
   - Evaluator's qualitative verdict
6. Highlight the biggest risk factor and the strongest asset

## Example
```
/evaluate-pair Darius Celine

Compatibility: 42%
  Big Five: 68% (both high openness)
  Traits: 55% (intelligence gap)
  Attachment: 25% (anxious + avoidant = classic trap)
  Strategy: 100% (both long-term)

Gottman Risk:
  Criticism: 38%  Contempt: 55%  Defensiveness: 52%  Stonewalling: 62%
  Ratio: 2.1:1 (below 5:1 threshold)
  Stability: 34/100 — Likely to dissolve

Biggest risk: Anxious-avoidant attachment trap
Strongest asset: Shared intellectual curiosity
```
