"""
Artwork-related actions for the Museum Chatbot
Handles intelligent artwork search with natural, interpreted responses
"""
import os
import sys
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Add utils to path
utils_path = os.path.join(os.path.dirname(__file__), 'utils')
if utils_path not in sys.path:
    sys.path.insert(0, utils_path)

from utils import (
    setup_logger,
    extract_artwork_from_message,
    wikipedia_client,
    summarize_wikipedia_content,
    extract_artist_from_wikipedia,
    detect_user_language,
    get_response_template,
    ARTWORK_INFO,
    clean_artwork_name # Added missing import
)

logger = setup_logger(__name__)


class ActionFetchArtworkPure(Action):
    """Intelligent artwork search with natural, interpreted responses"""
    
    def name(self) -> Text:
        return "action_fetch_artwork"
    
    def create_natural_response(self, dispatcher: CollectingDispatcher, wiki_data: Dict, artwork_name: str, user_language: str = 'de'):
        """Creates natural, interpreted responses instead of raw data output"""
        
        artwork_key = artwork_name.lower()
        
        # Begin with title and artist
        title = wiki_data.get('title', artwork_name) if wiki_data else artwork_name
        
        if artwork_key in ARTWORK_INFO:
            info = ARTWORK_INFO[artwork_key]
            artist = info['artist']
            
            # Beautiful introduction with templates
            intro_template = get_response_template(user_language, 'artwork_intro')
            created_template = get_response_template(user_language, 'artwork_created')
            
            message = intro_template.format(title=title, artist=artist)
            if info['year']:
                if user_language == 'de':
                    message += f" um **{info['year']}** "
                else:
                    message += f" around **{info['year']}** "
            message += created_template + "\n\n"
            
            # Wikipedia summary (interpreted)
            if wiki_data and wiki_data.get('extract'):
                summary = summarize_wikipedia_content(wiki_data['extract'], artwork_name)
                if summary:
                    about_template = get_response_template(user_language, 'about_artwork')
                    message += f"{about_template}\n{summary}\n\n"
              # Technical details beautifully packaged
            did_you_know_template = get_response_template(user_language, 'did_you_know')
            
            # Interesting fact
            message += f"{did_you_know_template}\n{info['fun_fact']}\n"
        
        else:
            # Fallback for unknown artworks
            artist = "Unbekannter Künstler" if user_language == 'de' else "Unknown Artist"
            
            # Try to extract artist from Wikipedia
            if wiki_data and wiki_data.get('extract'):
                extracted_artist = extract_artist_from_wikipedia(
                    wiki_data['extract'], 
                    wiki_data.get('language', user_language)
                )
                if extracted_artist != "Unbekannter Künstler":
                    artist = extracted_artist
            
            message = f"🎨 **{title}**\n\n"
            
            if artist != ("Unbekannter Künstler" if user_language == 'de' else "Unknown Artist"):
                remarkable_template = get_response_template(user_language, 'remarkable_artwork')
                message += remarkable_template.format(artist=artist) + "\n\n"
            
            # Wikipedia summary
            if wiki_data and wiki_data.get('extract'):
                summary = summarize_wikipedia_content(wiki_data['extract'], artwork_name)
                if summary:
                    about_template = get_response_template(user_language, 'about_artwork')
                    message += f"{about_template}\n{summary}\n\n"
            
            artist_label_template = get_response_template(user_language, 'artist_label')
            message += f"{artist_label_template} {artist}\n"
          # Send the beautifully formatted response
        dispatcher.utter_message(text=message)
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        user_language = detect_user_language(user_message)
        
        artwork_name_slot = tracker.get_slot("artwork_name")
        # Always try to extract from the message, as slot might be stale or less specific
        artwork_name_intent = extract_artwork_from_message(user_message)
        
        # Prioritize intent extraction if it's more specific or slot is missing
        if artwork_name_intent and (not artwork_name_slot or len(artwork_name_intent) > len(artwork_name_slot)):
            artwork_name = artwork_name_intent
            logger.info(f"Using artwork name from intent extraction: '{artwork_name}' (Slot was: '{artwork_name_slot}')")
        elif artwork_name_slot:
            artwork_name = artwork_name_slot
            logger.info(f"Using artwork name from slot: '{artwork_name}' (Intent extraction was: '{artwork_name_intent}')")
        else:
            artwork_name = artwork_name_intent # Fallback to intent if slot is also empty

        if not artwork_name or len(artwork_name) <= 2: # Check for empty or too short (e.g. just "Der")
            logger.warning(f"Artwork name is too short or empty after extraction: '{artwork_name}'. User message: '{user_message}'")
            no_artwork_template = get_response_template(user_language, 'no_artwork_specified')
            dispatcher.utter_message(text=no_artwork_template)
            return []
        
        # Clean the final artwork name one last time before search
        artwork_name_for_search = clean_artwork_name(artwork_name)
        logger.info(f"Suche nach Kunstwerk: '{artwork_name_for_search}' (Original extracted: '{artwork_name}', Language: {user_language})")
        
        try:
            # Wikipedia search with improved validation
            wiki_data = wikipedia_client.search_artwork(artwork_name_for_search)
            
            if wiki_data and wiki_data.get('extract'):
                logger.info(f"Wikipedia data found for '{artwork_name_for_search}'. Creating natural response.")
                # Use the most accurate title from Wikipedia if available, otherwise the searched name
                display_artwork_name = wiki_data.get('title', artwork_name_for_search)
                self.create_natural_response(dispatcher, wiki_data, display_artwork_name, user_language)
            else:
                logger.warning(f"No valid Wikipedia data found for '{artwork_name_for_search}'.")
                not_found_template = get_response_template(user_language, 'artwork_not_found')
                # Display the name the user originally asked for, if possible, for clarity
                dispatcher.utter_message(text=not_found_template.format(artwork_name=artwork_name))
                
        except Exception as e:
            logger.error(f"Fehler bei Kunstwerk-Suche: {e}")
            technical_error_template = get_response_template(user_language, 'technical_error')
            dispatcher.utter_message(text=technical_error_template)
        
        return []
