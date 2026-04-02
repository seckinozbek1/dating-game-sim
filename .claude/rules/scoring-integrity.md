---
paths:
  - "src/models/**"
---
# Scoring Model Integrity

## Compatibility Scores
- All scores must be in [0, 1] range
- Cosine similarity is the default for vector comparisons (Big Five, trait vectors)
- Attachment compatibility uses the empirical matrix, not computed similarity

## Gottman Scoring
- Four Horsemen are derived from personality interaction, not conversation text (for now)
- Criticism = f(neuroticism, low agreeableness)
- Contempt = f(low attachment compatibility, neuroticism)
- Defensiveness = f(neuroticism, low agreeableness)
- Stonewalling = f(low stability, avoidant attachment)
- Positive/negative ratio threshold is 5:1 per Gottman (1994)

## Weight Justification
| Weight | Value | Justification |
|--------|-------|---------------|
| Big Five similarity | 0.25 | Assortative mating literature: moderate predictor |
| Trait similarity | 0.20 | Li et al.: secondary to attachment |
| Attachment compat | 0.35 | Hazan & Shaver: strongest predictor of relationship quality |
| Strategy alignment | 0.20 | Buss & Schmitt: mismatch is a dealbreaker |

## Anti-Patterns
- Never clamp scores to avoid extreme results. If a pairing scores 15/100, report it.
- Never add "bonus points" for dramatic pairings. The math is the math.
