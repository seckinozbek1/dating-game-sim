---
name: create-agent
description: Create a new dating agent with a psychologically valid profile. Use when user says "add an agent", "create a new character", "new contestant", or "add personality".
argument-hint: "[name] [archetype]"
---

# Create Agent

## Steps
1. Ask for or infer:
   - Name
   - Archetype (1-word summary)
   - A 2-sentence description of who this person is
2. Generate a psychologically consistent profile:
   - Big Five scores (must be internally coherent — e.g., high agreeableness + low neuroticism = secure, not anxious)
   - Attachment style (must follow from Big Five pattern)
   - Mate value traits (kindness, intelligence, attractiveness, status, humor, stability)
   - Mating strategy (long-term or short-term)
   - Bio (2-3 sentences capturing their dating persona)
3. Validate consistency:
   - Anxious-preoccupied attachment requires neuroticism > 55
   - Dismissive-avoidant requires agreeableness < 60 or extraversion < 45
   - Secure requires neuroticism < 50 and agreeableness > 55
   - Short-term strategy correlates with high extraversion and openness
4. Add to src/agents/personas.json
5. Update CLAUDE.md agent quick reference table
6. Run a test: `/evaluate-pair [new_agent] [existing_agent]` to verify scoring works
