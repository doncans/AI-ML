"""Physical appearance and body language questions."""

APPEARANCE_QUESTIONS = [
    {
        "id": "app_1",
        "question": "How would you describe your typical posture?",
        "type": "single_choice",
        "options": [
            "Upright and confident",
            "Relaxed and casual",
            "Varies depending on the situation",
            "Tend to slouch or lean",
            "Very conscious about maintaining good posture",
        ],
        "traits": {
            "Upright and confident": {"confidence": 5, "self_discipline": 4, "assertiveness": 4},
            "Relaxed and casual": {"approachability": 5, "easygoing": 5, "comfort_seeking": 4},
            "Varies depending on the situation": {"adaptability": 5, "social_awareness": 4},
            "Tend to slouch or lean": {"casualness": 4, "comfort_seeking": 5, "low_energy": 3},
            "Very conscious about maintaining good posture": {"self_discipline": 5, "health_consciousness": 4, "self_awareness": 5},
        },
    },
    {
        "id": "app_2",
        "question": "How much do you use hand gestures when talking?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Almost never", "Rarely", "Sometimes", "Often", "Constantly"],
        "trait_mapping": {
            "expressiveness": "linear",
            "energy_level": "linear",
            "enthusiasm": "linear",
        },
    },
    {
        "id": "app_3",
        "question": "How important is personal grooming to you?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Not important", "Somewhat", "Moderate", "Important", "Extremely important"],
        "trait_mapping": {
            "self_care": "linear",
            "attention_to_detail": "linear",
            "self_presentation": "linear",
        },
    },
    {
        "id": "app_4",
        "question": "When meeting someone new, your body language tends to be:",
        "type": "single_choice",
        "options": [
            "Open and welcoming (arms open, leaning in)",
            "Warm but reserved (smile, polite distance)",
            "Nervous or fidgety",
            "Cool and composed",
            "Mirroring the other person's energy",
        ],
        "traits": {
            "Open and welcoming (arms open, leaning in)": {"warmth": 5, "social_openness": 5, "confidence": 4},
            "Warm but reserved (smile, polite distance)": {"politeness": 5, "boundaries": 4, "warmth": 3},
            "Nervous or fidgety": {"social_anxiety": 4, "sensitivity": 4, "self_consciousness": 4},
            "Cool and composed": {"emotional_control": 5, "confidence": 4, "guardedness": 3},
            "Mirroring the other person's energy": {"empathy": 5, "adaptability": 5, "emotional_intelligence": 5},
        },
    },
    {
        "id": "app_5",
        "question": "How aware are you of your own body language?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Not aware", "Slightly", "Somewhat", "Very aware", "Hyper-aware"],
        "trait_mapping": {
            "self_awareness": "linear",
            "mindfulness": "linear",
            "social_intelligence": "linear",
        },
    },
]
