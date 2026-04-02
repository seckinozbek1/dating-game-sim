---
paths:
  - "src/agents/**"
  - "src/prompts/**"
---
# Agent Persona Consistency

## Rules
1. An agent's system prompt MUST reflect their Big Five scores mechanically:
   - Extraversion > 70: speaks more, initiates, uses exclamation marks
   - Extraversion < 40: shorter responses, asks questions, pauses
   - Agreeableness > 80: accommodating, avoids conflict, uses "we"
   - Agreeableness < 40: blunt, challenges, uses "I"
   - Neuroticism > 65: shows anxiety, second-guesses, hedges
   - Neuroticism < 35: calm, steady, minimal emotional language
   - Openness > 80: abstract language, metaphors, creative tangents
   - Openness < 40: concrete, practical, literal

2. Attachment style MUST affect conversational behavior:
   - Secure: balanced self-disclosure, comfortable with silence
   - Anxious-preoccupied: seeks validation, reads into signals, escalates quickly
   - Dismissive-avoidant: deflects personal questions, intellectualizes emotion
   - Fearful-avoidant: hot-cold pattern, approach then retreat

3. Mating strategy affects what agents look for:
   - Long-term: asks about values, reliability, life goals
   - Short-term: focuses on fun, chemistry, immediate attraction

## Verification
After modifying any persona, run a test conversation and check:
- Does the output "sound" like the personality profile?
- Would a psychology student identify the attachment style from the conversation?
