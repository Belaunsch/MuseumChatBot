#!/usr/bin/env python3
"""
Test configuration for the Museum Guide Chatbot
Centralized configuration for all test components
"""

# Server configuration
SERVER_CONFIG = {
    "url": "http://localhost:5005",
    "timeout": 30,
    "health_check_timeout": 5,
    "delay_between_tests": 1.0  # seconds between tests
}

# File paths
TEST_RESULTS_FILE = "test_results.json"

# Test behavior
VERBOSE_OUTPUT = True
SHOW_DEBUG_INFO = True

# Evaluation criteria for response assessment
EVALUATION_CRITERIA = {
    "error_indicators": [
        "entschuldigung", "fehler", "error", "sorry",
        "keine informationen", "nicht finden", "konnte nicht", "leider nicht"
    ],
    "no_results_indicators": [
        "keine informationen", "nicht finden", "no information", "not found"
    ],
    "category_criteria": {
        "artwork": [
            "künstler:", "entstehung:", "material:", "🎨", 
            "beschreibung:", "quelle:", "technik:", "zu finden im:",
            "artist:", "created:", "medium:"
        ],
        "artist": [
            "geboren", "gestorben", "biografie:", "👨‍🎨", 
            "lebensdaten:", "bekannt als:", "nationalität",
            "born", "died", "biography:"
        ],
        "museum": [
            "öffnungszeiten:", "adresse:", "preis", "🏛️", 
            "📍", "💰", "bewertung:", "standort",
            "opening hours:", "address:", "price:", "rating:"
        ],
        "conversation": {
            "min_length": 10  # minimum length for meaningful response
        }
    },
    "api_sources": {
        "wikipedia": {
            "name": "Wikipedia API",
            "emoji": "📚",
            "indicators": ["Wikipedia", "wikipedia"]
        },
        "met_museum": {
            "name": "MET Museum API", 
            "emoji": "🏛️",
            "indicators": ["Metropolitan Museum", "MET Museum"]
        },
        "google_places": {
            "name": "Google Places API",
            "emoji": "📍", 
            "indicators": ["Google Places"]
        }
    }
}
