"""Facial expression and emotional display questions."""

FACIAL_EXPRESSION_QUESTIONS = [
    {
        "id": "face_1",
        "question": "How expressive are your facial expressions typically?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Very reserved", "Somewhat reserved", "Moderate", "Expressive", "Highly animated"],
        "trait_mapping": {
            "expressiveness": "linear",
            "emotional_openness": "linear",
            "extraversion": "scaled_0.7",
        },
    },
    {
        "id": "face_2",
        "question": "When you're happy, how do you usually show it?",
        "type": "single_choice",
        "options": [
            "Big smile and laughter",
            "Subtle smile and warm eyes",
            "Verbal expression ('I'm so happy!')",
            "Physical gestures (jumping, clapping, dancing)",
            "I feel it internally but don't show much",
        ],
        "traits": {
            "Big smile and laughter": {"expressiveness": 5, "extraversion": 5, "warmth": 5},
            "Subtle smile and warm eyes": {"emotional_depth": 4, "restraint": 4, "warmth": 4},
            "Verbal expression ('I'm so happy!')": {"verbal_orientation": 5, "social_engagement": 4},
            "Physical gestures (jumping, clapping, dancing)": {"physical_expressiveness": 5, "spontaneity": 5, "energy_level": 5},
            "I feel it internally but don't show much": {"introversion": 5, "emotional_guardedness": 4, "depth_seeking": 4},
        },
    },
    {
        "id": "face_3",
        "question": "How well can you read other people's facial expressions?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Poorly", "Below average", "Average", "Well", "Extremely well"],
        "trait_mapping": {
            "empathy": "linear",
            "emotional_intelligence": "linear",
            "social_awareness": "linear",
        },
    },
    {
        "id": "face_4",
        "question": "When you're upset or angry, your face usually:",
        "type": "single_choice",
        "options": [
            "Shows it clearly — everyone can tell",
            "Shows subtle signs (tight jaw, narrowed eyes)",
            "Stays neutral — I have a good poker face",
            "Smiles to mask the discomfort",
            "I'm told I look angry even when I'm not",
        ],
        "traits": {
            "Shows it clearly — everyone can tell": {"expressiveness": 5, "authenticity": 5, "emotional_transparency": 5},
            "Shows subtle signs (tight jaw, narrowed eyes)": {"self_awareness": 4, "partial_restraint": 4},
            "Stays neutral — I have a good poker face": {"emotional_control": 5, "guardedness": 5, "composure": 5},
            "Smiles to mask the discomfort": {"people_pleasing": 4, "conflict_avoidance": 4, "social_masking": 5},
            "I'm told I look angry even when I'm not": {"intensity": 4, "resting_expression_awareness": 3},
        },
    },
    {
        "id": "face_5",
        "question": "How much eye contact do you maintain during conversations?",
        "type": "single_choice",
        "options": [
            "Strong, consistent eye contact",
            "Regular eye contact with natural breaks",
            "Occasional glances, mostly look elsewhere",
            "Minimal — I find it uncomfortable",
            "It depends on who I'm talking to",
        ],
        "traits": {
            "Strong, consistent eye contact": {"confidence": 5, "assertiveness": 4, "presence": 5},
            "Regular eye contact with natural breaks": {"social_comfort": 4, "balance_seeking": 4, "emotional_intelligence": 4},
            "Occasional glances, mostly look elsewhere": {"introversion": 4, "thoughtfulness": 3, "anxiety_tendency": 3},
            "Minimal — I find it uncomfortable": {"social_anxiety": 4, "introversion": 5, "sensitivity": 4},
            "It depends on who I'm talking to": {"adaptability": 5, "social_awareness": 4, "contextual_intelligence": 5},
        },
    },
]
