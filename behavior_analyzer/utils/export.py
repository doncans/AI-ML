"""Export utilities for behavioral analysis reports."""

import json
from datetime import datetime
from typing import Any


def export_report_to_json(report: dict[str, Any]) -> str:
    """Export the full report as a formatted JSON string."""
    export_data = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "tool": "Human Behavior Analysis Agent",
            "author": "Sudhakar Donkena",
        },
        "analysis": report,
    }
    return json.dumps(export_data, indent=2, default=str)


def generate_text_summary(report: dict[str, Any]) -> str:
    """Generate a plain-text summary of the behavioral analysis."""
    lines = []
    lines.append("=" * 60)
    lines.append("HUMAN BEHAVIOR ANALYSIS REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)

    archetype = report.get("archetype", {})
    lines.append(f"\nBehavioral Archetype: {archetype.get('name', 'Unknown')}")
    lines.append(f"Description: {archetype.get('description', '')}")

    if archetype.get("strengths"):
        lines.append("\nStrengths:")
        for s in archetype["strengths"]:
            lines.append(f"  - {s}")

    if archetype.get("growth_areas"):
        lines.append("\nGrowth Areas:")
        for g in archetype["growth_areas"]:
            lines.append(f"  - {g}")

    lines.append("\n" + "-" * 40)
    lines.append("PERSONALITY PROFILE (Big Five)")
    lines.append("-" * 40)
    for dimension, data in report.get("personality_profile", {}).items():
        lines.append(f"  {dimension}: {data['score']:.0f}%")

    lines.append("\n" + "-" * 40)
    lines.append("TOP BEHAVIORAL TRAITS")
    lines.append("-" * 40)
    for trait, score in report.get("top_traits", []):
        lines.append(f"  {trait.replace('_', ' ').title()}: {score:.2f}/5")

    insights = report.get("insights", {})
    if insights:
        lines.append("\n" + "-" * 40)
        lines.append("PERSONALIZED INSIGHTS")
        lines.append("-" * 40)
        for category, insight in insights.items():
            lines.append(f"\n  [{category}]")
            lines.append(f"  {insight}")

    lines.append("\n" + "=" * 60)
    lines.append(f"Questions Answered: {report.get('total_questions_answered', 0)}")
    lines.append(f"Traits Analyzed: {report.get('total_traits_detected', 0)}")
    lines.append("=" * 60)

    return "\n".join(lines)
