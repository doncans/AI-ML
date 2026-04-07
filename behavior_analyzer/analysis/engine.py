"""Behavioral analysis engine that processes responses and generates profiles."""

from collections import defaultdict
from typing import Any

import numpy as np


PERSONALITY_DIMENSIONS = {
    "Openness": {
        "traits": [
            "adventurousness", "creativity", "curiosity", "cultural_curiosity",
            "cultural_exposure", "openness_to_experience", "flexibility",
            "self_expression", "individuality", "non_conformity",
        ],
        "description": "Reflects imagination, curiosity, and willingness to try new things.",
    },
    "Conscientiousness": {
        "traits": [
            "discipline", "organization", "planning", "thoroughness",
            "self_discipline", "routine_oriented", "attention_to_detail",
            "goal_oriented", "precision", "consistency",
        ],
        "description": "Indicates self-discipline, orderliness, and goal-directed behavior.",
    },
    "Extraversion": {
        "traits": [
            "extraversion", "social_engagement", "social_openness",
            "social_orientation", "expressiveness", "warmth",
            "confidence", "assertiveness", "energy_level", "enthusiasm",
        ],
        "description": "Measures sociability, assertiveness, and positive emotionality.",
    },
    "Agreeableness": {
        "traits": [
            "empathy", "warmth", "approachability", "altruism",
            "diplomacy", "peace_seeking", "politeness", "fairness",
            "community_orientation", "relationship_focus",
        ],
        "description": "Reflects cooperation, trust, and concern for others.",
    },
    "Emotional Stability": {
        "traits": [
            "emotional_control", "composure", "resilience", "self_confidence",
            "emotional_maturity", "emotional_intelligence", "mindfulness",
            "self_awareness", "balance_seeking", "adaptability",
        ],
        "description": "Indicates emotional regulation, calmness, and stress management.",
    },
}

BEHAVIORAL_ARCHETYPES = {
    "The Explorer": {
        "key_traits": ["adventurousness", "cultural_curiosity", "openness_to_experience", "spontaneity", "flexibility"],
        "description": "Thrives on new experiences, embraces uncertainty, and seeks out diverse perspectives.",
        "strengths": ["Adaptable", "Open-minded", "Culturally aware", "Quick learner"],
        "growth_areas": ["May struggle with routine", "Can be restless", "Might lack follow-through"],
    },
    "The Analyst": {
        "key_traits": ["analytical_thinking", "planning", "thoroughness", "organization", "precision"],
        "description": "Values data, logic, and structure. Approaches life methodically and thoroughly.",
        "strengths": ["Detail-oriented", "Strategic thinker", "Reliable", "Thorough"],
        "growth_areas": ["May overthink", "Can be inflexible", "Might miss emotional cues"],
    },
    "The Connector": {
        "key_traits": ["empathy", "social_engagement", "relationship_focus", "warmth", "emotional_intelligence"],
        "description": "Natural at building relationships. Prioritizes human connection and understanding.",
        "strengths": ["Empathetic", "Great communicator", "Team builder", "Socially aware"],
        "growth_areas": ["May people-please", "Can neglect self-care", "Might avoid confrontation"],
    },
    "The Leader": {
        "key_traits": ["leadership", "confidence", "assertiveness", "discipline", "goal_oriented"],
        "description": "Takes charge naturally. Driven by goals and comfortable with authority.",
        "strengths": ["Decisive", "Visionary", "Inspiring", "Results-oriented"],
        "growth_areas": ["May be domineering", "Can overlook details", "Might dismiss others' input"],
    },
    "The Creator": {
        "key_traits": ["creativity", "self_expression", "expressiveness", "individuality", "emotional_depth"],
        "description": "Driven by self-expression and originality. Sees the world through a unique lens.",
        "strengths": ["Innovative", "Expressive", "Imaginative", "Authentic"],
        "growth_areas": ["May be impractical", "Can be moody", "Might struggle with structure"],
    },
    "The Guardian": {
        "key_traits": ["tradition_value", "community_orientation", "rootedness", "discipline", "consistency"],
        "description": "Values stability, tradition, and community. Reliable and protective of close bonds.",
        "strengths": ["Dependable", "Loyal", "Grounded", "Protective"],
        "growth_areas": ["May resist change", "Can be rigid", "Might be overly cautious"],
    },
    "The Harmonizer": {
        "key_traits": ["balance_seeking", "peace_seeking", "diplomacy", "adaptability", "mindfulness"],
        "description": "Seeks balance in all things. Natural mediator who values inner and outer peace.",
        "strengths": ["Balanced", "Calming presence", "Good mediator", "Self-aware"],
        "growth_areas": ["May avoid decisions", "Can be passive", "Might suppress own needs"],
    },
    "The Achiever": {
        "key_traits": ["ambition", "discipline", "efficiency_focus", "goal_oriented", "self_discipline"],
        "description": "Focused on accomplishment and results. Driven by personal and professional growth.",
        "strengths": ["Productive", "Ambitious", "Focused", "Self-motivated"],
        "growth_areas": ["May be workaholic", "Can neglect relationships", "Might burn out"],
    },
}


class BehaviorAnalyzer:
    """Analyzes questionnaire responses and generates behavioral profiles."""

    def __init__(self) -> None:
        self.trait_scores: dict[str, list[float]] = defaultdict(list)
        self.category_completion: dict[str, bool] = {}
        self.raw_responses: dict[str, Any] = {}

    def process_response(
        self,
        question: dict[str, Any],
        response: Any,
    ) -> None:
        """Process a single question response and extract trait scores."""
        self.raw_responses[question["id"]] = response
        q_type = question["type"]

        if q_type == "single_choice" and response in question.get("traits", {}):
            traits = question["traits"][response]
            for trait, value in traits.items():
                if isinstance(value, (int, float)):
                    self.trait_scores[trait].append(float(value))

        elif q_type == "scale":
            scale_value = float(response)
            for trait, mapping in question.get("trait_mapping", {}).items():
                if mapping == "linear":
                    self.trait_scores[trait].append(scale_value)
                elif mapping.startswith("scaled_"):
                    factor = float(mapping.split("_")[1])
                    self.trait_scores[trait].append(scale_value * factor)

        elif q_type == "multi_choice" and isinstance(response, list):
            for selected in response:
                if selected in question.get("traits", {}):
                    traits = question["traits"][selected]
                    for trait, value in traits.items():
                        if isinstance(value, (int, float)):
                            self.trait_scores[trait].append(float(value))

    def get_aggregated_traits(self) -> dict[str, float]:
        """Return averaged trait scores."""
        return {
            trait: float(np.mean(scores))
            for trait, scores in self.trait_scores.items()
            if scores
        }

    def get_personality_profile(self) -> dict[str, dict[str, Any]]:
        """Calculate Big Five personality dimension scores."""
        traits = self.get_aggregated_traits()
        profile = {}

        for dimension, config in PERSONALITY_DIMENSIONS.items():
            dimension_traits = config["traits"]
            matching_scores = [
                traits[t] for t in dimension_traits if t in traits
            ]
            if matching_scores:
                score = float(np.mean(matching_scores))
                normalized = min(score / 5.0 * 100, 100)
                profile[dimension] = {
                    "score": round(normalized, 1),
                    "description": config["description"],
                    "contributing_traits": {
                        t: round(traits[t], 2)
                        for t in dimension_traits
                        if t in traits
                    },
                }
            else:
                profile[dimension] = {
                    "score": 0,
                    "description": config["description"],
                    "contributing_traits": {},
                }

        return profile

    def get_archetype(self) -> tuple[str, dict[str, Any]]:
        """Determine the closest behavioral archetype."""
        traits = self.get_aggregated_traits()
        best_archetype = ""
        best_score = -1.0

        for archetype, config in BEHAVIORAL_ARCHETYPES.items():
            key_traits = config["key_traits"]
            matching = [traits.get(t, 0) for t in key_traits]
            if matching:
                score = float(np.mean(matching))
                if score > best_score:
                    best_score = score
                    best_archetype = archetype

        archetype_info = BEHAVIORAL_ARCHETYPES.get(best_archetype, {})
        return best_archetype, {
            "score": round(best_score, 2),
            "description": archetype_info.get("description", ""),
            "strengths": archetype_info.get("strengths", []),
            "growth_areas": archetype_info.get("growth_areas", []),
        }

    def get_top_traits(self, n: int = 10) -> list[tuple[str, float]]:
        """Return the top N dominant traits."""
        traits = self.get_aggregated_traits()
        sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
        return [(t, round(s, 2)) for t, s in sorted_traits[:n]]

    def get_category_insights(self) -> dict[str, str]:
        """Generate natural language insights for each answered category."""
        traits = self.get_aggregated_traits()
        insights = {}

        geo_traits = {t: traits[t] for t in ["adaptability", "cultural_exposure", "rootedness"] if t in traits}
        if geo_traits:
            top = max(geo_traits, key=geo_traits.get)
            insight_map = {
                "adaptability": "You're highly adaptable and comfortable navigating unfamiliar environments.",
                "cultural_exposure": "Your diverse experiences have given you a broad cultural perspective.",
                "rootedness": "You value deep connections to place and community.",
            }
            insights["Geographic Profile"] = insight_map.get(top, "Your geographic background shapes your worldview.")

        food_traits = {t: traits[t] for t in ["health_consciousness", "social_bonding", "adventurousness"] if t in traits}
        if food_traits:
            top = max(food_traits, key=food_traits.get)
            insight_map = {
                "health_consciousness": "Food is fuel for you — you make thoughtful, health-focused choices.",
                "social_bonding": "Meals are social events for you — sharing food is how you connect.",
                "adventurousness": "You're a culinary explorer who loves trying new flavors and cuisines.",
            }
            insights["Food & Lifestyle"] = insight_map.get(top, "Your food habits reflect your personal values.")

        comm_traits = {t: traits[t] for t in ["empathy", "assertiveness", "introversion"] if t in traits}
        if comm_traits:
            top = max(comm_traits, key=comm_traits.get)
            insight_map = {
                "empathy": "You're an empathetic communicator who listens deeply and responds with care.",
                "assertiveness": "You communicate with confidence and aren't afraid to state your position.",
                "introversion": "You're thoughtful and selective in conversations, preferring depth over breadth.",
            }
            insights["Communication Style"] = insight_map.get(top, "Your communication style is a key part of who you are.")

        expr_traits = {t: traits[t] for t in ["expressiveness", "emotional_control", "social_awareness"] if t in traits}
        if expr_traits:
            top = max(expr_traits, key=expr_traits.get)
            insight_map = {
                "expressiveness": "Your emotions are written on your face — you communicate authentically.",
                "emotional_control": "You have strong emotional composure and reveal emotions selectively.",
                "social_awareness": "You're highly attuned to others' emotions and social dynamics.",
            }
            insights["Emotional Expression"] = insight_map.get(top, "Your emotional expression reflects your inner life.")

        body_traits = {t: traits[t] for t in ["confidence", "self_awareness", "approachability"] if t in traits}
        if body_traits:
            top = max(body_traits, key=body_traits.get)
            insight_map = {
                "confidence": "Your body language projects confidence and commands attention.",
                "self_awareness": "You're highly aware of how you present yourself physically.",
                "approachability": "Your open body language makes others feel comfortable around you.",
            }
            insights["Body Language"] = insight_map.get(top, "Your physical presence speaks volumes.")

        style_traits = {t: traits[t] for t in ["minimalism", "self_expression", "sophistication"] if t in traits}
        if style_traits:
            top = max(style_traits, key=style_traits.get)
            insight_map = {
                "minimalism": "Your minimalist style reflects a focus on substance over appearance.",
                "self_expression": "Fashion is your canvas — you use clothing to express your identity.",
                "sophistication": "You dress with polish and purpose, projecting a refined image.",
            }
            insights["Style & Fashion"] = insight_map.get(top, "Your style choices reveal your personal brand.")

        life_traits = {t: traits[t] for t in ["discipline", "spontaneity", "intellectual_curiosity"] if t in traits}
        if life_traits:
            top = max(life_traits, key=life_traits.get)
            insight_map = {
                "discipline": "Structure is your superpower — you thrive on routine and planning.",
                "spontaneity": "You embrace each day as it comes and thrive on variety.",
                "intellectual_curiosity": "You're a lifelong learner driven by curiosity and growth.",
            }
            insights["Daily Lifestyle"] = insight_map.get(top, "Your daily habits shape your success.")

        return insights

    def generate_full_report(self) -> dict[str, Any]:
        """Generate a comprehensive behavioral analysis report."""
        archetype_name, archetype_info = self.get_archetype()
        return {
            "personality_profile": self.get_personality_profile(),
            "archetype": {"name": archetype_name, **archetype_info},
            "top_traits": self.get_top_traits(10),
            "insights": self.get_category_insights(),
            "total_questions_answered": len(self.raw_responses),
            "total_traits_detected": len(self.get_aggregated_traits()),
        }
