"""
Utils package for Museum Chatbot Actions
Provides modular utilities for Wikipedia API, text processing, validation, and more
"""

from .logging_config import setup_logger, logger
from .mappings import (
    KNOWN_ARTWORKS, 
    KNOWN_ARTISTS, 
    WIKIPEDIA_ARTWORK_MAPPINGS, 
    ARTWORK_INFO
)
from .text_cleaner import (
    clean_artwork_name,
    clean_artist_name,
    extract_artwork_from_message,
    extract_artist_from_message
)
from .validation import (
    is_artwork_content,
    calculate_relevance_score,
    calculate_artist_relevance
)
from .summarizer import (
    summarize_wikipedia_content,
    summarize_artist_biography,
    extract_artist_from_wikipedia,
    extract_biographical_info,
    clean_text_content
)
from .wikipedia_client import WikipediaClient, wikipedia_client
from .language_detector import (
    detect_user_language,
    get_response_template,
    language_detector,
    RESPONSE_TEMPLATES
)

__all__ = [
    # Logging
    'setup_logger',
    'logger',
    
    # Mappings
    'KNOWN_ARTWORKS',
    'KNOWN_ARTISTS',
    'WIKIPEDIA_ARTWORK_MAPPINGS',
    'ARTWORK_INFO',
    
    # Text cleaning
    'clean_artwork_name',
    'clean_artist_name',
    'extract_artwork_from_message',
    'extract_artist_from_message',
    
    # Validation
    'is_artwork_content',
    'calculate_relevance_score',
    'calculate_artist_relevance',    # Summarization
    'summarize_wikipedia_content',
    'summarize_artist_biography',
    'extract_artist_from_wikipedia',
    'extract_biographical_info',
    'clean_text_content',
    
    # Wikipedia client
    'WikipediaClient',
    'wikipedia_client',
    
    # Language detection
    'detect_user_language',
    'get_response_template',
    'language_detector',
    'RESPONSE_TEMPLATES'
]