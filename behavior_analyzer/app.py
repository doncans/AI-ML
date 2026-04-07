"""
Human Behavior Analysis Agent
==============================
An interactive Chainlit chatbot that analyzes human behavior patterns
through conversational questionnaires across multiple behavioral categories.

Author: Sudhakar Donkena
Version: 1.0.0
"""

import io
import json
import logging
from datetime import datetime

import chainlit as cl

from behavior_analyzer.analysis.engine import BehaviorAnalyzer
from behavior_analyzer.analysis.visualizations import (
    create_dimension_breakdown,
    create_personality_radar,
    create_trait_bar_chart,
)
from behavior_analyzer.questions import ALL_CATEGORIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CATEGORIES = list(ALL_CATEGORIES.keys())
CATEGORY_ICONS = {
    "Geographic & Cultural Background": "📍",
    "Food Habits & Preferences": "🍽️",
    "Conversation & Communication Style": "💬",
    "Facial Expressions & Emotions": "😊",
    "Physical Appearance & Body Language": "🧍",
    "Dressing Style & Fashion": "👔",
    "Gender & Social Identity": "🌐",
    "Daily Activities & Lifestyle": "🏃",
}


def _fig_to_element(fig, name: str) -> cl.Image:
    """Convert a matplotlib figure to a Chainlit Image element."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    return cl.Image(content=buf.read(), name=name, display="inline")


async def _ask_single_choice(question: dict) -> str | None:
    """Ask a single-choice question using action buttons."""
    options = question["options"]
    actions = [
        cl.Action(name="answer", label=opt, payload={"value": opt})
        for opt in options
    ]
    res = await cl.AskActionMessage(
        content=f"**{question['question']}**",
        actions=actions,
        timeout=300,
    ).send()
    if res and res.get("payload"):
        return res["payload"]["value"]
    return None


async def _ask_scale(question: dict) -> int | None:
    """Ask a scale question using numbered action buttons."""
    scale_min = question["scale_min"]
    scale_max = question["scale_max"]
    labels = question.get("scale_labels", [])

    label_hint = ""
    if labels:
        label_hint = f"\n*({labels[0]} → {labels[-1]})*"

    actions = []
    for val in range(scale_min, scale_max + 1):
        label_text = str(val)
        if labels and 0 <= val - scale_min < len(labels):
            label_text = f"{val} - {labels[val - scale_min]}"
        actions.append(
            cl.Action(name="answer", label=label_text, payload={"value": str(val)})
        )

    res = await cl.AskActionMessage(
        content=f"**{question['question']}**{label_hint}\n\nRate from {scale_min} to {scale_max}:",
        actions=actions,
        timeout=300,
    ).send()
    if res and res.get("payload"):
        return int(res["payload"]["value"])
    return None


async def _ask_multi_choice(question: dict) -> list[str]:
    """Ask a multi-choice question by letting user type comma-separated numbers."""
    options = question["options"]
    options_text = "\n".join(f"  {i+1}. {opt}" for i, opt in enumerate(options))

    res = await cl.AskUserMessage(
        content=(
            f"**{question['question']}**\n\n"
            f"{options_text}\n\n"
            f"Type the numbers of your choices, separated by commas (e.g. `1,3,4`):"
        ),
        timeout=300,
    ).send()

    if res and res.get("output"):
        selected = []
        for part in res["output"].split(","):
            part = part.strip()
            if part.isdigit():
                idx = int(part) - 1
                if 0 <= idx < len(options):
                    selected.append(options[idx])
        return selected if selected else [options[0]]
    return [options[0]]


async def _ask_question(question: dict) -> object:
    """Route to the appropriate question handler based on type."""
    q_type = question["type"]
    if q_type == "single_choice":
        return await _ask_single_choice(question)
    elif q_type == "scale":
        return await _ask_scale(question)
    elif q_type == "multi_choice":
        return await _ask_multi_choice(question)
    return None


async def _generate_report(analyzer: BehaviorAnalyzer) -> None:
    """Generate and display the full behavioral analysis report."""
    report = analyzer.generate_full_report()

    # Archetype
    archetype = report["archetype"]
    archetype_msg = (
        f"# 🎭 Your Behavioral Archetype: **{archetype['name']}**\n\n"
        f"*{archetype['description']}*\n\n"
    )

    strengths = archetype.get("strengths", [])
    growth = archetype.get("growth_areas", [])
    if strengths:
        archetype_msg += "### 💪 Strengths\n"
        for s in strengths:
            archetype_msg += f"- {s}\n"
    if growth:
        archetype_msg += "\n### 🌱 Growth Areas\n"
        for g in growth:
            archetype_msg += f"- {g}\n"

    await cl.Message(content=archetype_msg).send()

    # Personality Profile charts
    profile = report["personality_profile"]

    radar_fig = create_personality_radar(profile)
    radar_img = _fig_to_element(radar_fig, "personality_radar")

    breakdown_fig = create_dimension_breakdown(profile)
    breakdown_img = _fig_to_element(breakdown_fig, "dimension_breakdown")

    await cl.Message(
        content="## 📊 Personality Profile (Big Five)",
        elements=[radar_img, breakdown_img],
    ).send()

    # Top Traits chart
    trait_fig = create_trait_bar_chart(report["top_traits"])
    trait_img = _fig_to_element(trait_fig, "top_traits")

    await cl.Message(
        content="## 🏆 Top Behavioral Traits",
        elements=[trait_img],
    ).send()

    # Detailed dimension scores
    dimensions_msg = "## 📋 Detailed Dimension Scores\n\n"
    for dimension, data in profile.items():
        score = data["score"]
        bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        dimensions_msg += f"**{dimension}**: {score:.0f}%\n`{bar}`\n"
        dimensions_msg += f"*{data['description']}*\n\n"
    await cl.Message(content=dimensions_msg).send()

    # Category Insights
    insights = report.get("insights", {})
    if insights:
        insights_msg = "## 💡 Personalized Insights\n\n"
        for category, insight in insights.items():
            insights_msg += f"### {category}\n{insight}\n\n"
        await cl.Message(content=insights_msg).send()

    # Summary stats
    summary_msg = (
        "## 📈 Analysis Summary\n\n"
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| Questions Answered | {report['total_questions_answered']} |\n"
        f"| Traits Analyzed | {report['total_traits_detected']} |\n"
        f"| Categories Covered | {len(CATEGORIES)} |\n"
        f"| Archetype | {archetype['name']} |\n"
    )
    await cl.Message(content=summary_msg).send()

    # Export JSON
    report_json = json.dumps(report, indent=2, default=str)
    json_bytes = report_json.encode("utf-8")
    filename = f"behavior_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    file_element = cl.File(name=filename, content=json_bytes, display="inline")
    await cl.Message(
        content="## 📥 Download Your Full Report\nHere is your complete behavioral analysis report in JSON format:",
        elements=[file_element],
    ).send()

    # Offer retake
    retake_actions = [
        cl.Action(name="retake", label="🔄 Retake Assessment", payload={"value": "retake"}),
    ]
    await cl.AskActionMessage(
        content="Would you like to retake the assessment?",
        actions=retake_actions,
        timeout=600,
    ).send()


@cl.on_chat_start
async def on_chat_start():
    """Handle new chat session - display welcome and start questionnaire."""
    welcome_msg = (
        "# 🧠 Human Behavior Analysis Agent\n\n"
        "*Discover your behavioral patterns, personality traits, and unique archetype*\n\n"
        "I'll ask you **40 questions** across **8 categories**:\n\n"
    )
    for cat in CATEGORIES:
        icon = CATEGORY_ICONS.get(cat, "📌")
        welcome_msg += f"- {icon} {cat}\n"

    welcome_msg += (
        "\nThis takes about **5-8 minutes**. "
        "Your responses will be analyzed to create a comprehensive behavioral profile.\n\n"
        "---"
    )
    await cl.Message(content=welcome_msg).send()

    # Start questionnaire
    actions = [
        cl.Action(name="start", label="🚀 Start Analysis", payload={"value": "start"}),
    ]
    res = await cl.AskActionMessage(
        content="Ready to begin?",
        actions=actions,
        timeout=600,
    ).send()

    if res:
        await run_questionnaire()


async def run_questionnaire():
    """Run through all categories and questions, then generate report."""
    analyzer = BehaviorAnalyzer()
    responses = {}
    total_questions = sum(len(qs) for qs in ALL_CATEGORIES.values())
    question_num = 0

    for cat_idx, (category, questions) in enumerate(ALL_CATEGORIES.items()):
        icon = CATEGORY_ICONS.get(category, "📌")
        progress_pct = int((question_num / total_questions) * 100)
        progress_bar = "█" * (progress_pct // 5) + "░" * (20 - progress_pct // 5)

        await cl.Message(
            content=(
                f"---\n"
                f"## {icon} Category {cat_idx + 1}/8: {category}\n"
                f"Progress: `{progress_bar}` {progress_pct}%"
            )
        ).send()

        for q_idx, question in enumerate(questions):
            question_num += 1
            q_label = f"**Q{question_num}/{total_questions}**"
            await cl.Message(content=f"{q_label}").send()

            response = await _ask_question(question)

            if response is not None:
                responses[question["id"]] = response
                analyzer.process_response(question, response)

                # Show confirmation
                if isinstance(response, list):
                    display = ", ".join(response)
                else:
                    display = str(response)
                await cl.Message(
                    content=f"✓ *{display}*",
                    author="You",
                ).send()

        await cl.Message(
            content=f"✅ **{category}** complete!"
        ).send()

    # Generate analysis
    await cl.Message(
        content=(
            "---\n"
            "# 🔍 Generating Your Behavioral Analysis...\n\n"
            "Processing your responses across all 8 categories..."
        )
    ).send()

    cl.user_session.set("analyzer", analyzer)
    cl.user_session.set("responses", responses)

    await _generate_report(analyzer)


@cl.action_callback("retake")
async def on_retake(action: cl.Action):
    """Handle retake assessment action."""
    await cl.Message(content="Starting a fresh assessment...").send()
    await run_questionnaire()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle free-text messages during the session."""
    text = message.content.strip().lower()
    if text in ("start", "begin", "restart", "retake"):
        await run_questionnaire()
    else:
        await cl.Message(
            content=(
                "I'm your **Human Behavior Analysis Agent**. "
                "Type **start** to begin or retake the assessment, "
                "or click the buttons above to interact."
            )
        ).send()
