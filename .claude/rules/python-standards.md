---
paths:
  - "**/*.py"
---
# Python Code Standards

## Style
- Type hints on all function signatures
- Docstrings on all public functions (include theory reference if scoring-related)
- f-strings for formatting, no .format() or %

## Structure
- Keep LLM calls in src/prompts/ — never inline API calls in model code
- Keep scoring math in src/models/ — never compute scores inside prompt builders
- Agent definitions live in personas.json, not hardcoded in Python

## Error Handling
- Wrap all Anthropic API calls in try/except
- If API fails, log the error and return a fallback (e.g., random selection instead of LLM ranking)
- Never crash the simulation on a single failed API call
