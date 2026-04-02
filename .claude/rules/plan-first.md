# Plan-First Workflow

## When to Plan
Enter plan mode before:
- Adding a new agent or modifying personality profiles
- Changing scoring formulas or compatibility weights
- Adding new psychological theories to the model
- Restructuring the simulation flow

## When to Skip Planning
- Bug fixes under 10 lines
- Typo corrections
- Adding print/logging statements

## Plan Format
Save plans to `quality_reports/plans/YYYY-MM-DD_description.md` with:
- Goal (1 sentence)
- Approach (numbered steps)
- Files to modify
- Psychological basis (which theories are involved)
- Verification (how to confirm it works)
