"""Question banks for behavioral analysis categories."""

from behavior_analyzer.questions.geography import GEOGRAPHY_QUESTIONS
from behavior_analyzer.questions.food import FOOD_QUESTIONS
from behavior_analyzer.questions.conversation import CONVERSATION_QUESTIONS
from behavior_analyzer.questions.facial_expressions import FACIAL_EXPRESSION_QUESTIONS
from behavior_analyzer.questions.appearance import APPEARANCE_QUESTIONS
from behavior_analyzer.questions.dressing import DRESSING_QUESTIONS
from behavior_analyzer.questions.gender import GENDER_QUESTIONS
from behavior_analyzer.questions.activities import ACTIVITY_QUESTIONS

ALL_CATEGORIES = {
    "Geographic & Cultural Background": GEOGRAPHY_QUESTIONS,
    "Food Habits & Preferences": FOOD_QUESTIONS,
    "Conversation & Communication Style": CONVERSATION_QUESTIONS,
    "Facial Expressions & Emotions": FACIAL_EXPRESSION_QUESTIONS,
    "Physical Appearance & Body Language": APPEARANCE_QUESTIONS,
    "Dressing Style & Fashion": DRESSING_QUESTIONS,
    "Gender & Social Identity": GENDER_QUESTIONS,
    "Daily Activities & Lifestyle": ACTIVITY_QUESTIONS,
}

__all__ = ["ALL_CATEGORIES"]
