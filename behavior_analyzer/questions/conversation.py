"""Conversation and communication style questions."""

CONVERSATION_QUESTIONS = [
    {
        "id": "conv_1",
        "question": "In a group conversation, you typically:",
        "type": "single_choice",
        "options": [
            "Lead the discussion and set the topic",
            "Actively participate and share opinions",
            "Listen carefully and contribute occasionally",
            "Prefer one-on-one conversations over groups",
            "Stay quiet and observe others",
        ],
        "traits": {
            "Lead the discussion and set the topic": {"leadership": 5, "confidence": 5, "extraversion": 5},
            "Actively participate and share opinions": {"assertiveness": 4, "social_engagement": 4, "extraversion": 4},
            "Listen carefully and contribute occasionally": {"thoughtfulness": 4, "empathy": 4, "balance_seeking": 4},
            "Prefer one-on-one conversations over groups": {"depth_seeking": 5, "introversion": 4, "intimacy_preference": 5},
            "Stay quiet and observe others": {"introversion": 5, "analytical_thinking": 4, "observer_nature": 5},
        },
    },
    {
        "id": "conv_2",
        "question": "When you disagree with someone, you tend to:",
        "type": "single_choice",
        "options": [
            "Speak up directly and debate the point",
            "Express disagreement diplomatically",
            "Ask questions to understand their perspective first",
            "Agree outwardly but hold your position privately",
            "Avoid the conflict entirely",
        ],
        "traits": {
            "Speak up directly and debate the point": {"assertiveness": 5, "confidence": 5, "directness": 5},
            "Express disagreement diplomatically": {"emotional_intelligence": 5, "diplomacy": 5, "maturity": 4},
            "Ask questions to understand their perspective first": {"empathy": 5, "curiosity": 5, "open_mindedness": 5},
            "Agree outwardly but hold your position privately": {"conflict_avoidance": 4, "independence": 3, "guardedness": 4},
            "Avoid the conflict entirely": {"conflict_avoidance": 5, "peace_seeking": 5, "anxiety_tendency": 3},
        },
    },
    {
        "id": "conv_3",
        "question": "Your preferred communication style is:",
        "type": "single_choice",
        "options": [
            "Face-to-face conversation",
            "Phone/video calls",
            "Text messages/chat",
            "Email (detailed and thoughtful)",
            "Social media comments/posts",
        ],
        "traits": {
            "Face-to-face conversation": {"interpersonal_comfort": 5, "emotional_intelligence": 4, "presence": 5},
            "Phone/video calls": {"social_engagement": 4, "efficiency_focus": 3},
            "Text messages/chat": {"convenience_preference": 4, "control_preference": 3},
            "Email (detailed and thoughtful)": {"analytical_thinking": 5, "thoroughness": 5, "introversion": 3},
            "Social media comments/posts": {"digital_comfort": 5, "public_expression": 4},
        },
    },
    {
        "id": "conv_4",
        "question": "How comfortable are you with silence in conversations?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Very uncomfortable", "Uneasy", "Neutral", "Comfortable", "Completely at ease"],
        "trait_mapping": {
            "emotional_maturity": "linear",
            "self_confidence": "linear",
            "mindfulness": "linear",
        },
    },
    {
        "id": "conv_5",
        "question": "When telling a story, you tend to:",
        "type": "single_choice",
        "options": [
            "Give every detail in chronological order",
            "Focus on the emotional highlights",
            "Keep it brief and to the point",
            "Use humor and exaggeration",
            "Let others tell the story instead",
        ],
        "traits": {
            "Give every detail in chronological order": {"thoroughness": 5, "analytical_thinking": 4, "precision": 5},
            "Focus on the emotional highlights": {"emotional_intelligence": 5, "empathy": 4, "expressiveness": 5},
            "Keep it brief and to the point": {"efficiency_focus": 5, "directness": 5, "minimalism": 4},
            "Use humor and exaggeration": {"creativity": 5, "social_engagement": 5, "playfulness": 5},
            "Let others tell the story instead": {"introversion": 4, "modesty": 5, "observer_nature": 4},
        },
    },
]
