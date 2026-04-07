"""Visualization functions for behavioral analysis reports."""

from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")


def create_personality_radar(profile: dict[str, dict[str, Any]]) -> plt.Figure:
    """Create a radar chart for Big Five personality dimensions."""
    categories = list(profile.keys())
    values = [profile[c]["score"] for c in categories]

    n = len(categories)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})

    ax.fill(angles, values_plot, color="#4A90D9", alpha=0.25)
    ax.plot(angles, values_plot, color="#4A90D9", linewidth=2.5)
    ax.scatter(angles[:-1], values_plot[:-1], color="#4A90D9", s=80, zorder=5)

    for angle, value in zip(angles[:-1], values):
        ax.text(
            angle, value + 5, f"{value:.0f}%",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color="#2C3E50",
        )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight="bold", color="#2C3E50")
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=8, color="grey")
    ax.grid(color="grey", linestyle="-", linewidth=0.5, alpha=0.3)
    ax.set_title("Personality Profile", fontsize=16, fontweight="bold", color="#2C3E50", pad=20)

    plt.tight_layout()
    return fig


def create_trait_bar_chart(top_traits: list[tuple[str, float]]) -> plt.Figure:
    """Create a horizontal bar chart for top behavioral traits."""
    traits = [t[0].replace("_", " ").title() for t in reversed(top_traits)]
    scores = [t[1] for t in reversed(top_traits)]

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(traits)))
    bars = ax.barh(traits, scores, color=colors, edgecolor="white", linewidth=0.5, height=0.7)

    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
            f"{score:.1f}", va="center", fontsize=10, fontweight="bold", color="#2C3E50",
        )

    ax.set_xlim(0, 5.5)
    ax.set_xlabel("Score (out of 5)", fontsize=12, color="#2C3E50")
    ax.set_title("Top Behavioral Traits", fontsize=16, fontweight="bold", color="#2C3E50")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="y", labelsize=11)

    plt.tight_layout()
    return fig


def create_dimension_breakdown(profile: dict[str, dict[str, Any]]) -> plt.Figure:
    """Create a detailed breakdown chart for each personality dimension."""
    n_dims = len(profile)
    fig, axes = plt.subplots(1, n_dims, figsize=(4 * n_dims, 5))

    if n_dims == 1:
        axes = [axes]

    colors = ["#E74C3C", "#F39C12", "#2ECC71", "#3498DB", "#9B59B6"]

    for idx, (dimension, data) in enumerate(profile.items()):
        ax = axes[idx]
        score = data["score"]

        wedge_sizes = [score, 100 - score]
        wedge_colors = [colors[idx % len(colors)], "#ECECEC"]

        ax.pie(
            wedge_sizes,
            startangle=90,
            colors=wedge_colors,
            wedgeprops={"width": 0.35, "edgecolor": "white", "linewidth": 2},
        )

        ax.text(0, 0, f"{score:.0f}%", ha="center", va="center", fontsize=20, fontweight="bold", color=colors[idx % len(colors)])
        ax.set_title(dimension, fontsize=11, fontweight="bold", color="#2C3E50", pad=10)

    fig.suptitle("Personality Dimensions Breakdown", fontsize=16, fontweight="bold", color="#2C3E50", y=1.02)
    plt.tight_layout()
    return fig
