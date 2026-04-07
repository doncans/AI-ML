"""Geographic and cultural background questions."""

GEOGRAPHY_QUESTIONS = [
    {
        "id": "geo_1",
        "question": "Which region do you currently live in?",
        "type": "single_choice",
        "options": [
            "Urban metropolitan city",
            "Suburban area",
            "Small town",
            "Rural/countryside",
            "Coastal area",
            "Mountain/highland region",
        ],
        "traits": {
            "Urban metropolitan city": {"social_openness": 4, "adaptability": 5, "pace_of_life": 5},
            "Suburban area": {"social_openness": 3, "adaptability": 3, "pace_of_life": 3},
            "Small town": {"social_openness": 3, "adaptability": 2, "community_orientation": 5},
            "Rural/countryside": {"social_openness": 2, "adaptability": 2, "nature_connection": 5},
            "Coastal area": {"social_openness": 3, "adaptability": 3, "nature_connection": 4},
            "Mountain/highland region": {"social_openness": 2, "adaptability": 3, "nature_connection": 5},
        },
    },
    {
        "id": "geo_2",
        "question": "How many different cities/countries have you lived in?",
        "type": "single_choice",
        "options": ["1 (hometown only)", "2-3", "4-5", "More than 5"],
        "traits": {
            "1 (hometown only)": {"cultural_exposure": 1, "adaptability": 2, "rootedness": 5},
            "2-3": {"cultural_exposure": 3, "adaptability": 3, "rootedness": 3},
            "4-5": {"cultural_exposure": 4, "adaptability": 4, "rootedness": 2},
            "More than 5": {"cultural_exposure": 5, "adaptability": 5, "rootedness": 1},
        },
    },
    {
        "id": "geo_3",
        "question": "What climate do you prefer?",
        "type": "single_choice",
        "options": [
            "Tropical and warm",
            "Temperate and mild",
            "Cold and snowy",
            "Dry and arid",
            "I adapt to any climate",
        ],
        "traits": {
            "Tropical and warm": {"energy_level": 4, "outdoor_preference": 4},
            "Temperate and mild": {"energy_level": 3, "balance_seeking": 4},
            "Cold and snowy": {"introversion": 3, "indoor_preference": 4},
            "Dry and arid": {"resilience": 4, "minimalism": 3},
            "I adapt to any climate": {"adaptability": 5, "flexibility": 5},
        },
    },
    {
        "id": "geo_4",
        "question": "How connected do you feel to your cultural heritage?",
        "type": "scale",
        "scale_min": 1,
        "scale_max": 5,
        "scale_labels": ["Not at all", "Slightly", "Moderately", "Strongly", "Deeply connected"],
        "trait_mapping": {
            "cultural_identity": "linear",
            "tradition_value": "linear",
            "rootedness": "linear",
        },
    },
    {
        "id": "geo_5",
        "question": "How do you typically navigate in a new city?",
        "type": "single_choice",
        "options": [
            "GPS/maps app always",
            "Ask locals for directions",
            "Explore and wander freely",
            "Research extensively before going",
            "Follow a planned itinerary",
        ],
        "traits": {
            "GPS/maps app always": {"tech_reliance": 5, "planning": 4},
            "Ask locals for directions": {"social_openness": 5, "interpersonal_comfort": 4},
            "Explore and wander freely": {"adventurousness": 5, "spontaneity": 5},
            "Research extensively before going": {"analytical_thinking": 5, "planning": 5},
            "Follow a planned itinerary": {"organization": 5, "planning": 4},
        },
    },
]
