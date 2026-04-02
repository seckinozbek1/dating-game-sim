# CLAUDE.MD — Dating Game Agent Simulation

**Project:** LLM-Powered Dating Game Simulation
**Purpose:** Multi-agent dating simulation grounded in relationship psychology research

## Core Principles
1. **Plan-first** — enter plan mode before non-trivial changes
2. **Psychology-grounded** — every mechanic must cite a theory (Gottman, Buss, Bowlby, etc.)
3. **Verify-after** — run the simulation and check output before reporting done
4. **LEARN tags** — persist corrections and discoveries in MEMORY.md

## Folder Structure
```
dating_game/
├── CLAUDE.md                    ← you are here
├── MEMORY.md                    ← persistent corrections
├── README.md                    ← project overview + setup
├── .claude/
│   ├── settings.json            ← permissions
│   ├── rules/                   ← auto-loading rules
│   ├── skills/                  ← slash commands
│   └── agents/                  ← reviewer agents
├── src/
│   ├── agents/                  ← agent personality definitions
│   │   └── personas.json        ← the 5 candidate profiles
│   ├── models/
│   │   ├── selection.py         ← mate selection engine
│   │   ├── compatibility.py     ← Gottman-based scoring
│   │   └── dynamics.py          ← simulation round logic
│   ├── prompts/
│   │   ├── agent_system.py      ← agent system prompt builder
│   │   └── evaluator_system.py  ← relationship evaluator prompt
│   └── main.py                  ← entry point
├── output/                      ← simulation results
└── quality_reports/
    ├── plans/
    └── session_logs/
```

## Key Commands
| Command | What It Does |
|---------|-------------|
| `python src/main.py` | Run full simulation |
| `python src/main.py --picker Ayla` | Run with specific picker |
| `python src/main.py --rounds 5` | Multi-round simulation |
| `pip install anthropic --break-system-packages` | Install Anthropic SDK |

## Current State
| Component | Status |
|-----------|--------|
| Agent personas (5) | ✅ Done |
| Selection engine (SVR + assortative) | ✅ Done |
| Gottman evaluator | ✅ Done |
| LLM conversation engine | ✅ Done |
| Multi-round dynamics | 🔲 Todo |
| Data export / analysis | 🔲 Todo |

## Theories Implemented
| Theory | Source | Used In |
|--------|--------|---------|
| Big Five personality | Costa & McCrae (1992) | Agent profiles |
| Attachment theory | Bowlby (1969), Hazan & Shaver (1987) | Compatibility matrix |
| Sexual Strategies Theory | Buss & Schmitt (1993) | Strategy alignment |
| SVR Theory | Murstein (1970) | Selection stages |
| Necessities vs Luxuries | Li et al. (2002) | Trait weighting |
| Four Horsemen | Gottman et al. (1998) | Relationship evaluation |
| 5:1 Ratio | Gottman (1994) | Stability prediction |
| Assortative mating | Review: Thiessen & Gregg (1980) | Similarity scoring |

## Agent Quick Reference
| Name | Archetype | Attachment | Strategy |
|------|-----------|------------|----------|
| Ayla | Adventurer | Secure | Short-term |
| Ben | Caretaker | Secure | Long-term |
| Celine | Intellectual | Dismissive-avoidant | Long-term |
| Darius | Romantic | Anxious-preoccupied | Long-term |
| Elena | Pragmatist | Secure | Long-term |
