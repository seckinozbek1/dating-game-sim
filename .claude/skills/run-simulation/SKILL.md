---
name: run-simulation
description: Run the full dating game simulation. Use when user says "run", "simulate", "start the game", or "let them date".
argument-hint: "[picker_name] [--rounds N]"
---

# Run Simulation

## Steps
1. Check that ANTHROPIC_API_KEY is set in the environment
2. If picker name is provided, validate it exists in personas.json
3. If no picker, prompt user to choose from the 5 agents
4. Run: `python src/main.py --picker $ARGUMENTS`
5. Review the output for:
   - Did all LLM calls succeed? (check for fallback messages)
   - Does the conversation sound in-character?
   - Are compatibility scores in valid range [0, 1]?
   - Is the Gottman stability score in [0, 100]?
6. Save results to output/ with timestamp

## Troubleshooting
- "API key not set": Run `$env:ANTHROPIC_API_KEY = "sk-ant-..."` (PowerShell) or `export ANTHROPIC_API_KEY=...` (bash)
- "ModuleNotFoundError: anthropic": Run `pip install anthropic`
- Conversation feels generic: Check that persona system prompts include Big Five scores
