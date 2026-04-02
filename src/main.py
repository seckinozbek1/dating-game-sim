"""
Dating Game Agent Simulation — Main Entry Point

Usage:
    python src/main.py                     # Run bar-night simulation (verbose by default)
    python src/main.py --quiet             # Minimal console output
    python src/main.py --annotate          # Add per-exchange psychological analysis
    python src/main.py --serve             # Run annotated simulation + open viewer in browser
"""

from __future__ import annotations
import argparse
import json
import re
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path so imports work
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.models.dynamics import run_bar_night
from config import MODEL

# Deterministic color assignment by agent id (display layer only)
AGENT_COLORS: dict[str, str] = {
    "T":  "#E8607A",   # Vera — rose
    "S1": "#5B9BD5",   # Marcus — blue
    "S2": "#E8A838",   # Theo — amber
    "S3": "#7B68C8",   # Elliot — violet
    "S4": "#4BAE8A",   # Rafael — teal
    "S5": "#E07B54",   # Dex — coral
}


def load_agents() -> dict[str, Any]:
    """Load agent personas. Returns dict with 'target' and 'suitors' keys."""
    personas_path = PROJECT_ROOT / "src" / "agents" / "personas.json"
    with open(personas_path) as f:
        return json.load(f)


def parse_ranking(ranking_text: str, agents: list[dict]) -> list[dict]:
    """
    Parse LLM ranking text into a structured array.

    Handles 5 entries. "None" as a name means the target chose nobody.
    Expected format: "1. Name - reaction text"
    """
    results = []
    agent_names = {a["name"].lower() for a in agents}
    for line in ranking_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(\d+)\.\s*([A-Za-z]+)\s*[-–]\s*(.+)$", line)
        if m:
            rank = int(m.group(1))
            name = m.group(2).strip()
            reaction = m.group(3).strip()
            results.append({
                "rank": rank,
                "name": name,
                "reaction": reaction,
                "is_rejection": name.lower() == "none",
            })
    results.sort(key=lambda x: x["rank"])
    return results


def build_enriched_bar_night(result: dict[str, Any]) -> dict[str, Any]:
    """
    Transform run_bar_night() output into the full viewer JSON schema.
    Adds color fields to all agent objects and parses the ranking text.
    """
    def enrich(agent: dict) -> dict:
        return {**agent, "color": AGENT_COLORS.get(agent["id"], "#888888")}

    target = enrich(result["target"])
    suitors = [enrich(s) for s in result["suitors"]]

    encounters = [
        {
            "suitor": enrich(enc["suitor"]),
            "conversation": enc["conversation"],
            "fatigue_at_start": enc["fatigue_at_start"],
        }
        for enc in result["encounters"]
    ]

    rankings = parse_ranking(result["ranking_text"], result["suitors"])
    chosen = enrich(result["chosen"]) if result["chosen"] is not None else None

    return {
        "meta": {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "model": MODEL,
            "scenario": "bar_night",
        },
        "target": target,
        "suitors": suitors,
        "encounters": encounters,
        "rankings": rankings,
        "chosen": chosen,
        "compatibility": result["compatibility"],
        "svr": result["svr"],
        "gottman": result["gottman"],
        "evaluation": result["evaluation"],
    }


def save_results(enriched: dict[str, Any]) -> Path:
    """Save enriched simulation results to output/ with timestamp."""
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scenario = enriched["meta"].get("scenario", "round")
    if scenario == "bar_night":
        filename = f"{timestamp}_bar_night_{enriched['target']['name']}.json"
    else:
        filename = f"{timestamp}_{enriched['picker']['name']}_x_{enriched['match']['name']}.json"
    filepath = output_dir / filename
    with open(filepath, "w") as f:
        json.dump(enriched, f, indent=2, default=str)
    return filepath


def write_viewer_data(enriched: dict[str, Any]) -> Path:
    """
    Write viewer/data.js so the HTML viewer can load the simulation result.

    Uses window.SIMULATION_DATA assignment because fetch() is blocked under
    file:// by Chrome/Firefox CORS policy. Same-directory <script src> works fine.
    """
    viewer_dir = PROJECT_ROOT / "viewer"
    viewer_dir.mkdir(exist_ok=True)
    data_js = viewer_dir / "data.js"
    payload = json.dumps(enriched, indent=2, default=str)
    data_js.write_text(f"window.SIMULATION_DATA = {payload};\n", encoding="utf-8")
    return viewer_dir / "index.html"


def main() -> None:
    parser = argparse.ArgumentParser(description="Dating Game — Bar Night Simulation")
    parser.add_argument("--verbose", action="store_true", default=True, help="Verbose output")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    parser.add_argument("--annotate", action="store_true", help="Add per-exchange LLM psychological analysis")
    parser.add_argument("--serve", action="store_true", help="Run annotated simulation and open viewer in browser (implies --annotate)")
    parser.add_argument("--agentic", action="store_true", help="Run agentic mode: agents use tool_use, dual-model, prompt caching")
    args = parser.parse_args()

    if args.quiet:
        args.verbose = False
    if args.serve:
        args.annotate = True

    # Check API key
    from config import ANTHROPIC_API_KEY
    if ANTHROPIC_API_KEY == "sk-ant-your-key-here":
        print("\n  ERROR: Update your API key in config.py")
        sys.exit(1)

    agents = load_agents()
    target = agents["target"]
    suitors = agents["suitors"]

    if args.agentic:
        from src.agentic_main import run_agentic_bar_night
        result = run_agentic_bar_night(target, suitors, verbose=args.verbose, annotate=args.annotate)
    else:
        result = run_bar_night(target, suitors, verbose=args.verbose, annotate=args.annotate)
    enriched = build_enriched_bar_night(result)
    filepath = save_results(enriched)
    print(f"\n  Results saved to: {filepath}")

    if args.annotate:
        write_viewer_data(enriched)
        print(f"  Viewer data written to: {PROJECT_ROOT / 'viewer' / 'data.js'}")

    if args.serve:
        viewer_url = (PROJECT_ROOT / "viewer" / "index.html").as_uri()
        print(f"  Opening viewer: {viewer_url}")
        webbrowser.open(viewer_url)

    print(f"\n{'='*60}")
    print("  Simulation complete.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
