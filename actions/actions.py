"""
Refactored Museum Chatbot Actions - Main Module
This module imports and exposes all actions from the modular structure:
- Artwork actions: ActionFetchArtworkPure
- Artist actions: ActionFetchArtistInfo  
- Greeting actions: ActionGreet, ActionGoodbye
- Museum actions: ActionFetchMuseumInfo

The refactor provides:
- Clean modular structure for better maintainability
- Centralized utilities for reuse across modules
- Improved testability and readability
- Preserved existing behavior
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import all actions from the modular structure
from artwork_actions import ActionFetchArtworkPure
from artist_actions import ActionFetchArtist
from greeting_actions import ActionGreet, ActionGoodbye
from museum_actions import ActionFetchMuseumInfo

# Import comprehensive actions for enhanced functionality
try:
    from comprehensive_actions import (
        ActionFetchArtInfo,
        ActionRecommendContent,
        ActionCompareArtworks,
        ActionSaveUserPreference,
        ActionHandleComplexQuery
    )
    comprehensive_actions_available = True
except ImportError:
    comprehensive_actions_available = False
    print("Comprehensive actions not available - using basic actions only")

# Export all actions for external use
if comprehensive_actions_available:
    __all__ = [
        'ActionFetchArtworkPure',
        'ActionFetchArtist',
        'ActionGreet',
        'ActionGoodbye',
        'ActionFetchMuseumInfo',
        'ActionFetchArtInfo',
        'ActionRecommendContent',
        'ActionCompareArtworks',
        'ActionSaveUserPreference',
        'ActionHandleComplexQuery'
    ]
else:
    __all__ = [
        'ActionFetchArtworkPure',
        'ActionFetchArtist',
        'ActionGreet',
        'ActionGoodbye',
        'ActionFetchMuseumInfo'
    ]
