"""Gender identity and social dynamics questions."""

GENDER_QUESTIONS = [
    {
        "id": "gen_1",
        "question": "How would you describe your gender identity?",
        "type": "single_choice",
        "options": [
            "Male",
            "Female",
            "Non-binary",
            "Gender fluid",
            "Prefer not to say",
            "Other",
        ],
        "traits": {
            "Male": {"gender_identity": "male"},
            "Female": {"gender_identity": "female"},
            "Non-binary": {"gender_identity": "non-binary", "non_conformity": 4},
            "Gender fluid": {"gender_identity": "fluid", "flexibility": 5, "non_conformity": 5},
            "Prefer not to say": {"privacy_value": 5},
            "Other": {"individuality": 5},
        },
    },
    {
        "id": "gen_2",
        "question": "How much do societal gender expectations influence your behavior?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Not at all", "Very little", "Somewhat", "Significantly", "Strongly"],
        "trait_mapping": {
            "social_conformity": "linear",
            "tradition_value": "linear",
            "external_validation": "linear",
        },
    },
    {
        "id": "gen_3",
        "question": "In mixed-gender group settings, you tend to:",
        "type": "single_choice",
        "options": [
            "Behave the same regardless of group composition",
            "Adapt your communication style slightly",
            "Feel more comfortable with your own gender",
            "Actively ensure inclusive participation",
            "Don't pay attention to gender dynamics",
        ],
        "traits": {
            "Behave the same regardless of group composition": {"authenticity": 5, "consistency": 5, "confidence": 4},
            "Adapt your communication style slightly": {"social_awareness": 5, "emotional_intelligence": 4, "adaptability": 4},
            "Feel more comfortable with your own gender": {"in_group_preference": 4, "comfort_seeking": 3},
            "Actively ensure inclusive participation": {"empathy": 5, "leadership": 4, "fairness": 5},
            "Don't pay attention to gender dynamics": {"pragmatism": 4, "task_focus": 4},
        },
    },
    {
        "id": "gen_4",
        "question": "How do you feel about traditional gender roles in the household?",
        "type": "single_choice",
        "options": [
            "Strongly support traditional roles",
            "Somewhat support with flexibility",
            "Neutral — whatever works for the household",
            "Prefer equal sharing of all responsibilities",
            "Actively challenge traditional roles",
        ],
        "traits": {
            "Strongly support traditional roles": {"tradition_value": 5, "structure_preference": 5},
            "Somewhat support with flexibility": {"balance_seeking": 4, "moderate": 4},
            "Neutral — whatever works for the household": {"pragmatism": 5, "flexibility": 4},
            "Prefer equal sharing of all responsibilities": {"fairness": 5, "egalitarianism": 5, "partnership_value": 5},
            "Actively challenge traditional roles": {"progressive": 5, "conviction": 5, "non_conformity": 4},
        },
    },
    {
        "id": "gen_5",
        "question": "How important is it for you to express yourself beyond gender norms?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Not important", "Slightly", "Moderately", "Important", "Very important"],
        "trait_mapping": {
            "self_expression": "linear",
            "individuality": "linear",
            "non_conformity": "linear",
        },
    },
]
