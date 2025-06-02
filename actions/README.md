# Museum Chatbot Actions - Refactored Structure

This document describes the refactored modular structure of the Museum Chatbot actions.

## Overview

The original monolithic `actions.py` file has been refactored into a clean, modular structure for better maintainability, testability, and readability.

## Structure

```
actions/
├── actions.py                 # Main module - imports and exposes all actions
├── artwork_actions.py         # Artwork-related actions
├── artist_actions.py          # Artist-related actions  
├── greeting_actions.py        # Greeting and farewell actions
├── museum_actions.py          # Museum information actions
└── utils/                     # Utility modules
    ├── __init__.py           # Package initialization and exports
    ├── logging_config.py     # Centralized logging configuration
    ├── mappings.py           # Known artworks and artists mappings
    ├── text_cleaner.py       # Text cleaning and normalization
    ├── validation.py         # Content validation and scoring
    ├── summarizer.py         # Text summarization and extraction
    └── wikipedia_client.py   # Wikipedia API client
```

## Modules Description

### Action Modules

- **`artwork_actions.py`**: Contains `ActionFetchArtworkPure` for intelligent artwork search
- **`artist_actions.py`**: Contains `ActionFetchArtistInfo` for artist information retrieval
- **`greeting_actions.py`**: Contains `ActionGreet` and `ActionGoodbye` for user interactions
- **`museum_actions.py`**: Contains `ActionFetchMuseumInfo` for museum information

### Utility Modules

- **`logging_config.py`**: Provides centralized logging setup with `setup_logger()` function
- **`mappings.py`**: Contains dictionaries for known artworks, artists, and artwork information
- **`text_cleaner.py`**: Functions for cleaning and extracting artwork/artist names from messages
- **`validation.py`**: Content validation functions to ensure Wikipedia results are art-related
- **`summarizer.py`**: Text summarization and biographical information extraction
- **`wikipedia_client.py`**: Encapsulates all Wikipedia API interactions

## Key Benefits

1. **Modularity**: Each module has a single responsibility
2. **Maintainability**: Easy to modify individual components without affecting others
3. **Testability**: Each module can be tested independently
4. **Reusability**: Utility functions can be imported by any action module
5. **Clean Imports**: Actions only import what they need
6. **Centralized Configuration**: Logging and mappings are centralized

## Usage

The refactored structure maintains full backward compatibility. Rasa will import actions from the main `actions.py` file exactly as before:

```python
from actions.actions import ActionFetchArtworkPure, ActionFetchArtistInfo
```

Individual modules can also be imported directly:

```python
from actions.artwork_actions import ActionFetchArtworkPure
from actions.utils import wikipedia_client, setup_logger
```

## Dependencies

The refactoring preserves all existing dependencies:
- `rasa_sdk`
- `requests` 
- `python-dotenv`
- Standard library modules (`re`, `urllib.parse`, `logging`, `typing`)

## Migration Notes

- All existing functionality is preserved
- No changes needed to Rasa configuration files
- Environment variables are still loaded via `python-dotenv`
- Logging behavior remains the same but is now centralized
- Wikipedia API calls are now encapsulated in a dedicated client class

## Testing

To test the refactored structure:

```bash
# Run the existing test suite
python test_chatbot.py

# Or test individual modules
python -c "from actions.utils import wikipedia_client; print('Import successful')"
python -c "from actions.actions import ActionFetchArtworkPure; print('Actions import successful')"
```
