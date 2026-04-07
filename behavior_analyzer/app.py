"""
Human Behavior Analysis Agent
==============================
An interactive Streamlit application that analyzes human behavior patterns
through structured questionnaires across multiple behavioral categories.

Author: Sudhakar Donkena
Version: 1.0.0
"""

import json
import logging
from datetime import datetime
from pathlib import Path

import streamlit as st

from behavior_analyzer.analysis.engine import BehaviorAnalyzer
from behavior_analyzer.analysis.visualizations import (
    create_dimension_breakdown,
    create_personality_radar,
    create_trait_bar_chart,
)
from behavior_analyzer.questions import ALL_CATEGORIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Human Behavior Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .category-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2C3E50;
        padding: 0.5rem 0;
        border-bottom: 2px solid #4A90D9;
        margin-bottom: 1rem;
    }
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    .trait-badge {
        display: inline-block;
        background: #4A90D9;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 2px;
        font-size: 0.85rem;
    }
    .archetype-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1rem 0;
    }
    .progress-text {
        font-size: 0.9rem;
        color: #6c757d;
    }
    .stRadio > label {
        font-weight: 500;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "analyzer" not in st.session_state:
        st.session_state.analyzer = BehaviorAnalyzer()
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "current_category_idx" not in st.session_state:
        st.session_state.current_category_idx = 0
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "started" not in st.session_state:
        st.session_state.started = False


def render_landing_page() -> None:
    """Render the welcome/landing page."""
    st.markdown('<div class="main-header">Human Behavior Analysis Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Discover your behavioral patterns, personality traits, and unique archetype</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### 📍 Geography")
        st.caption("Cultural background & location influence")
    with col2:
        st.markdown("### 🍽️ Food Habits")
        st.caption("Dietary choices & eating patterns")
    with col3:
        st.markdown("### 💬 Communication")
        st.caption("Conversation & social style")
    with col4:
        st.markdown("### 😊 Expressions")
        st.caption("Facial cues & emotional display")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown("### 🧍 Body Language")
        st.caption("Posture, gestures & presence")
    with col6:
        st.markdown("### 👔 Dressing Style")
        st.caption("Fashion choices & self-presentation")
    with col7:
        st.markdown("### 🌐 Gender & Identity")
        st.caption("Social identity & dynamics")
    with col8:
        st.markdown("### 🏃 Daily Activities")
        st.caption("Routine, hobbies & lifestyle")

    st.markdown("---")

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.info("📋 **40 questions** across **8 categories** — takes about **5-8 minutes**")
        if st.button("🚀 Start Analysis", use_container_width=True, type="primary"):
            st.session_state.started = True
            st.rerun()


def render_question(question: dict, category_name: str) -> object | None:
    """Render a single question and return the response."""
    q_id = question["id"]
    q_type = question["type"]
    q_text = question["question"]

    existing = st.session_state.responses.get(q_id)

    if q_type == "single_choice":
        options = question["options"]
        default_idx = options.index(existing) if existing in options else 0
        response = st.radio(
            q_text,
            options=options,
            index=default_idx,
            key=f"q_{q_id}",
        )
        return response

    elif q_type == "scale":
        scale_min = question["scale_min"]
        scale_max = question["scale_max"]
        labels = question.get("scale_labels", [])
        default_val = existing if isinstance(existing, int) else 3

        label_text = ""
        if labels:
            label_text = f" ({labels[0]} → {labels[-1]})"

        response = st.slider(
            f"{q_text}{label_text}",
            min_value=scale_min,
            max_value=scale_max,
            value=default_val,
            key=f"q_{q_id}",
        )

        if labels and 0 <= response - scale_min < len(labels):
            st.caption(f"Your selection: **{labels[response - scale_min]}**")

        return response

    elif q_type == "multi_choice":
        options = question["options"]
        default = existing if isinstance(existing, list) else []
        response = st.multiselect(
            q_text,
            options=options,
            default=default,
            key=f"q_{q_id}",
        )
        return response

    return None


def render_questionnaire() -> None:
    """Render the interactive questionnaire."""
    categories = list(ALL_CATEGORIES.keys())
    n_categories = len(categories)
    current_idx = st.session_state.current_category_idx

    # Sidebar progress
    with st.sidebar:
        st.markdown("### Progress")
        progress = current_idx / n_categories
        st.progress(progress)
        st.caption(f"Category {current_idx + 1} of {n_categories}")

        st.markdown("---")
        st.markdown("### Categories")
        for idx, cat in enumerate(categories):
            if idx < current_idx:
                st.markdown(f"✅ {cat}")
            elif idx == current_idx:
                st.markdown(f"▶️ **{cat}**")
            else:
                st.markdown(f"⬜ {cat}")

        st.markdown("---")
        answered = len(st.session_state.responses)
        total = sum(len(qs) for qs in ALL_CATEGORIES.values())
        st.caption(f"Questions answered: {answered}/{total}")

    current_category = categories[current_idx]
    questions = ALL_CATEGORIES[current_category]

    st.markdown(f'<div class="category-header">{current_category}</div>', unsafe_allow_html=True)
    st.caption(f"Section {current_idx + 1} of {n_categories}")

    responses_this_category = {}
    for question in questions:
        response = render_question(question, current_category)
        if response is not None:
            responses_this_category[question["id"]] = response
        st.markdown("---")

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_idx > 0:
            if st.button("← Previous", use_container_width=True):
                for q_id, resp in responses_this_category.items():
                    st.session_state.responses[q_id] = resp
                st.session_state.current_category_idx -= 1
                st.rerun()

    with col3:
        if current_idx < n_categories - 1:
            if st.button("Next →", use_container_width=True, type="primary"):
                # Save responses
                for q_id, resp in responses_this_category.items():
                    st.session_state.responses[q_id] = resp
                st.session_state.current_category_idx += 1
                st.rerun()
        else:
            if st.button("🔍 Generate Analysis", use_container_width=True, type="primary"):
                for q_id, resp in responses_this_category.items():
                    st.session_state.responses[q_id] = resp
                # Process all responses
                analyzer = BehaviorAnalyzer()
                for cat_questions in ALL_CATEGORIES.values():
                    for question in cat_questions:
                        q_id = question["id"]
                        if q_id in st.session_state.responses:
                            analyzer.process_response(question, st.session_state.responses[q_id])
                st.session_state.analyzer = analyzer
                st.session_state.analysis_complete = True
                st.rerun()


def render_results() -> None:
    """Render the analysis results dashboard."""
    analyzer = st.session_state.analyzer
    report = analyzer.generate_full_report()

    st.markdown('<div class="main-header">Your Behavioral Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Based on your responses across 8 behavioral categories</div>',
        unsafe_allow_html=True,
    )

    # Archetype section
    archetype = report["archetype"]
    st.markdown(
        f"""<div class="archetype-box">
            <h2 style="margin:0;">You are: {archetype['name']}</h2>
            <p style="font-size:1.1rem; margin-top:0.5rem;">{archetype['description']}</p>
        </div>""",
        unsafe_allow_html=True,
    )

    # Strengths and growth areas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 💪 Your Strengths")
        for s in archetype.get("strengths", []):
            st.markdown(f"- {s}")
    with col2:
        st.markdown("#### 🌱 Growth Areas")
        for g in archetype.get("growth_areas", []):
            st.markdown(f"- {g}")

    st.markdown("---")

    # Personality Profile
    st.markdown("## Personality Profile (Big Five)")
    col_radar, col_breakdown = st.columns([1, 1])

    with col_radar:
        radar_fig = create_personality_radar(report["personality_profile"])
        st.pyplot(radar_fig)

    with col_breakdown:
        breakdown_fig = create_dimension_breakdown(report["personality_profile"])
        st.pyplot(breakdown_fig)

    st.markdown("---")

    # Top Traits
    st.markdown("## Top Behavioral Traits")
    trait_fig = create_trait_bar_chart(report["top_traits"])
    st.pyplot(trait_fig)

    st.markdown("---")

    # Category Insights
    st.markdown("## Personalized Insights")
    insights = report["insights"]
    if insights:
        cols = st.columns(2)
        for idx, (category, insight) in enumerate(insights.items()):
            with cols[idx % 2]:
                st.markdown(
                    f"""<div class="insight-card">
                        <h4 style="margin:0; color:white;">{category}</h4>
                        <p style="margin-top:0.5rem;">{insight}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # Detailed Personality Scores
    st.markdown("## Detailed Dimension Scores")
    for dimension, data in report["personality_profile"].items():
        with st.expander(f"{dimension} — {data['score']:.0f}%"):
            st.markdown(f"*{data['description']}*")
            st.progress(data["score"] / 100)
            if data["contributing_traits"]:
                st.markdown("**Contributing traits:**")
                for trait, score in data["contributing_traits"].items():
                    st.markdown(f"- {trait.replace('_', ' ').title()}: {score:.2f}/5")

    st.markdown("---")

    # Summary stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Answered", report["total_questions_answered"])
    with col2:
        st.metric("Traits Analyzed", report["total_traits_detected"])
    with col3:
        st.metric("Categories Covered", len(ALL_CATEGORIES))

    st.markdown("---")

    # Export
    col_export1, col_export2, col_export3 = st.columns([1, 1, 1])
    with col_export1:
        report_json = json.dumps(report, indent=2, default=str)
        st.download_button(
            "📥 Download Full Report (JSON)",
            data=report_json,
            file_name=f"behavior_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_export3:
        if st.button("🔄 Retake Assessment", use_container_width=True):
            st.session_state.responses = {}
            st.session_state.analyzer = BehaviorAnalyzer()
            st.session_state.current_category_idx = 0
            st.session_state.analysis_complete = False
            st.session_state.started = False
            st.rerun()


def main() -> None:
    """Main application entry point."""
    init_session_state()

    if st.session_state.analysis_complete:
        render_results()
    elif st.session_state.started:
        render_questionnaire()
    else:
        render_landing_page()


if __name__ == "__main__":
    main()
