#!/usr/bin/env python3
"""
Governance Maturity Assessment — evaluate your data governance program.

Usage:
    python3 scripts/governance-assessment.py
    python3 scripts/governance-assessment.py --json

Answers 15 scored questions across 5 dimensions. Produces a maturity level,
dimension scores, and prioritized recommendations. Outputs human-readable
text by default, or JSON with --json for machine consumption.
"""

import json
import sys
import textwrap

# === Scoring ===

DIMENSIONS = {
    "policy": "Policies & Standards",
    "roles": "Roles & Ownership",
    "tools": "Tooling & Metadata",
    "quality": "Data Quality",
    "culture": "Culture & Adoption",
}

QUESTIONS = [
    # (dimension, question, low_label, high_label)
    ("policy", "How are data governance policies documented?",
     "No formal policies", "Enterprise-wide policies, reviewed quarterly with automated enforcement"),
    ("policy", "How consistently are policies followed across teams?",
     "Ad hoc, varies by team", "Automated enforcement with audit trails"),
    ("policy", "How do you handle regulatory compliance requirements?",
     "Reactively when audited", "Proactive, automated compliance checks embedded in pipelines"),

    ("roles", "Who owns data quality and definitions?",
     "No clear ownership", "Dedicated data stewards per domain with formal charters"),
    ("roles", "How is data ownership assigned?",
     "No owners identified", "Every dataset has a documented owner with performance goals"),
    ("roles", "Is there a data governance council?",
     "No council exists", "Active council meeting monthly with executive sponsorship"),

    ("tools", "How do users discover and understand data?",
     "Ask colleagues or read source code", "Active metadata catalog with automated lineage and semantic search"),
    ("tools", "How is data lineage tracked?",
     "Not tracked", "Automated column-level lineage across all systems"),
    ("tools", "How do you manage metadata?",
     "Spreadsheets or shared docs", "Active metadata platform with automated ingestion and enrichment"),

    ("quality", "How do you measure data quality?",
     "Not measured systematically", "Automated quality dashboards with SLAs per dataset"),
    ("quality", "How are data quality issues detected and resolved?",
     "Found by users during analysis", "Automated monitoring with alerts and tiered SLAs"),
    ("quality", "How do you handle data quality at ingestion?",
     "No validation at entry", "Automated validation rules, schema enforcement, and anomaly detection"),

    ("culture", "How do teams perceive data governance?",
     "As a bottleneck or blocker", "As an enabler — governance makes data easier to use"),
    ("culture", "How is governance funded and resourced?",
     "Project-based, inconsistent", "Dedicated budget and headcount with executive sponsorship"),
    ("culture", "How does governance affect decision-making velocity?",
     "Slows teams down", "Faster decisions because trusted data is easier to find and use"),
]


def score_response(response):
    """Convert 1-5 response to a score."""
    try:
        val = int(response)
        if 1 <= val <= 5:
            return val
    except (ValueError, TypeError):
        pass
    return None


def text_prompt(dimension, question, low_label, high_label):
    """Present a question and get a 1-5 response."""
    print(f"\n--- {DIMENSIONS[dimension]} ---")
    print(f"Q: {question}")
    print(f"  1 = {low_label}")
    print(f"  5 = {high_label}")
    while True:
        try:
            resp = input("  Score (1-5): ").strip()
            score = score_response(resp)
            if score:
                return score
            print("  Please enter a number between 1 and 5.")
        except (EOFError, KeyboardInterrupt):
            print("\n  Assessment cancelled.")
            sys.exit(1)


def json_prompt():
    """Return placeholder scores for JSON mode (no interactivity)."""
    print("Run without --json for interactive assessment.", file=sys.stderr)
    sys.exit(0)


def calculate_maturity(avg_score):
    """Map average score to maturity level."""
    if avg_score < 1.5:
        return (0, "Unaware — no governance concept exists")
    elif avg_score < 2.5:
        return (1, "Initial — reactive, ad hoc, crisis-driven")
    elif avg_score < 3.5:
        return (2, "Managed — basic structures, siloed, early tools")
    elif avg_score < 4.0:
        return (3, "Defined — enterprise-wide, consistent, council-driven")
    elif avg_score < 4.5:
        return (4, "Integrated — embedded in workflows, automated enforcement")
    else:
        return (5, "Optimized — AI-driven, strategic, culture-embedded")


def generate_recommendations(scores):
    """Generate prioritized recommendations based on lowest scores."""
    dim_avgs = {}
    for dim in DIMENSIONS:
        dim_scores = [s for d, s in scores if d == dim]
        dim_avgs[dim] = sum(dim_scores) / len(dim_scores) if dim_scores else 0

    sorted_dims = sorted(dim_avgs.items(), key=lambda x: x[1])

    recommendations = []
    for dim, avg in sorted_dims:
        if avg < 2.0:
            recommendations.append(f"[HIGH] {DIMENSIONS[dim]}: avg {avg:.1f}/5 — Start with basic {dim.replace('_', ' ')}. See references/governance-maturity.md Level 0→1.")
        elif avg < 3.0:
            recommendations.append(f"[MEDIUM] {DIMENSIONS[dim]}: avg {avg:.1f}/5 — Formalize {dim.replace('_', ' ')}. See references/governance-maturity.md Level 2→3.")
        elif avg < 4.0:
            recommendations.append(f"[LOW] {DIMENSIONS[dim]}: avg {avg:.1f}/5 — Improve {dim.replace('_', ' ')} consistency. See references/governance-maturity.md Level 3→4.")
        else:
            recommendations.append(f"[MONITOR] {DIMENSIONS[dim]}: avg {avg:.1f}/5 — Maintain. See references/governance-maturity.md Level 4→5.")

    return recommendations


def main():
    json_mode = "--json" in sys.argv

    if json_mode:
        print(json.dumps({
            "error": "Run interactively without --json for assessment",
            "usage": "python3 scripts/governance-assessment.py"
        }, indent=2))
        return

    print("=" * 60)
    print("  Data Governance Maturity Assessment")
    print("=" * 60)
    print("  Rate each dimension from 1 (worst) to 5 (best).")
    print("  Be honest — the assessment is for you, not anyone else.")
    print("=" * 60)

    scores = []
    for dim, question, low, high in QUESTIONS:
        score = text_prompt(dim, question, low, high)
        scores.append((dim, score))

    # Calculate results
    dim_avgs = {}
    for dim in DIMENSIONS:
        dim_scores = [s for d, s in scores if d == dim]
        dim_avgs[dim] = sum(dim_scores) / len(dim_scores) if dim_scores else 0

    overall = sum(dim_avgs.values()) / len(dim_avgs)
    level, level_label = calculate_maturity(overall)

    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print(f"\n  Overall Maturity: Level {level} — {level_label}")
    print(f"  Average Score: {overall:.1f}/5\n")
    print("  Dimension Scores:")
    for dim in DIMENSIONS:
        bar = "█" * int(dim_avgs[dim]) + "░" * (5 - int(dim_avgs[dim]))
        print(f"    {DIMENSIONS[dim]:25s} {bar} {dim_avgs[dim]:.1f}/5")

    print("\n  Recommendations:")
    recs = generate_recommendations(scores)
    for r in recs:
        print(f"    {r}")

    print("\n  For detailed stage descriptions, see:")
    print("    references/governance-maturity.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
