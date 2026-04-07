"""Food habits and dietary preference questions."""

FOOD_QUESTIONS = [
    {
        "id": "food_1",
        "question": "How would you describe your eating pattern?",
        "type": "single_choice",
        "options": [
            "Strict meal schedule (breakfast, lunch, dinner)",
            "Eat when hungry, no fixed schedule",
            "Frequent small meals throughout the day",
            "Intermittent fasting or time-restricted eating",
            "One or two large meals a day",
        ],
        "traits": {
            "Strict meal schedule (breakfast, lunch, dinner)": {"discipline": 5, "routine_oriented": 5, "planning": 4},
            "Eat when hungry, no fixed schedule": {"spontaneity": 4, "flexibility": 4, "intuitive": 4},
            "Frequent small meals throughout the day": {"health_consciousness": 4, "self_awareness": 4},
            "Intermittent fasting or time-restricted eating": {"discipline": 5, "health_consciousness": 5, "willpower": 5},
            "One or two large meals a day": {"efficiency_focus": 4, "minimalism": 3},
        },
    },
    {
        "id": "food_2",
        "question": "What best describes your dietary preference?",
        "type": "single_choice",
        "options": [
            "Omnivore (eat everything)",
            "Vegetarian",
            "Vegan",
            "Pescatarian",
            "Flexitarian (mostly plant-based)",
            "Keto/Low-carb",
        ],
        "traits": {
            "Omnivore (eat everything)": {"flexibility": 4, "traditional": 3},
            "Vegetarian": {"empathy": 4, "ethical_awareness": 4, "health_consciousness": 4},
            "Vegan": {"empathy": 5, "ethical_awareness": 5, "discipline": 5, "conviction": 5},
            "Pescatarian": {"balance_seeking": 4, "health_consciousness": 4},
            "Flexitarian (mostly plant-based)": {"adaptability": 4, "balance_seeking": 5},
            "Keto/Low-carb": {"discipline": 5, "goal_oriented": 5, "health_consciousness": 5},
        },
    },
    {
        "id": "food_3",
        "question": "How adventurous are you with trying new foods?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Very cautious", "Somewhat cautious", "Open", "Adventurous", "Will try anything"],
        "trait_mapping": {
            "adventurousness": "linear",
            "openness_to_experience": "linear",
            "cultural_curiosity": "linear",
        },
    },
    {
        "id": "food_4",
        "question": "Do you prefer cooking at home or eating out?",
        "type": "single_choice",
        "options": [
            "Almost always cook at home",
            "Mostly home cooking, occasionally eat out",
            "Equal mix of both",
            "Mostly eat out or order delivery",
            "Almost never cook",
        ],
        "traits": {
            "Almost always cook at home": {"self_reliance": 5, "health_consciousness": 4, "creativity": 4},
            "Mostly home cooking, occasionally eat out": {"balance_seeking": 4, "self_reliance": 4},
            "Equal mix of both": {"flexibility": 4, "social_orientation": 3},
            "Mostly eat out or order delivery": {"social_orientation": 4, "convenience_preference": 4},
            "Almost never cook": {"convenience_preference": 5, "social_orientation": 4},
        },
    },
    {
        "id": "food_5",
        "question": "How important is sharing meals with others to you?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Not important", "Slightly", "Moderately", "Very important", "Essential"],
        "trait_mapping": {
            "social_bonding": "linear",
            "community_orientation": "linear",
            "relationship_focus": "linear",
        },
    },
]
