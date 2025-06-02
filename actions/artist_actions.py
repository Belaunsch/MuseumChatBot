"""
Artist-related actions for the Museum Chatbot
Handles intelligent artist search with natural, interpreted responses
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
    extract_artist_from_message,
    wikipedia_client,
    summarize_artist_biography,
    extract_biographical_info,
    detect_user_language,
    get_response_template
)
from utils.mappings import KNOWN_ARTISTS # Added import

logger = setup_logger(__name__)


class ActionFetchArtist(Action):
    """Intelligent artist search with natural, interpreted responses"""
    
    def name(self) -> Text:
        return "action_fetch_artist"
    
    def create_artist_response(self, dispatcher: CollectingDispatcher, wiki_data: Dict, artist_name: str, user_language: str = 'de'):
        """Creates natural, interpreted artist responses"""
        
        title = wiki_data.get('title', artist_name)
        
        # Extract biographical information including birth/death years
        extract = wiki_data.get('extract', '')
        bio_info = extract_biographical_info(extract, artist_name) if extract else {}
          # Create artist header with years if available
        artist_header = f"🎨 **{title}"
        years = []
        
        if bio_info.get('birth_date'):
            birth_year = str(bio_info['birth_date'])
            # Extract just the year if it's a full date
            if len(birth_year) > 4:
                import re
                year_match = re.search(r'\d{4}', birth_year)
                birth_year = year_match.group() if year_match else birth_year[:4]
            years.append(birth_year)
        
        if bio_info.get('death_date'):
            death_year = str(bio_info['death_date'])
            # Extract just the year if it's a full date
            if len(death_year) > 4:
                import re
                year_match = re.search(r'\d{4}', death_year)
                death_year = year_match.group() if year_match else death_year[:4]
            years.append(death_year)
        
        if years:
            if len(years) == 2:
                artist_header += f" ({years[0]}–{years[1]})"
            elif len(years) == 1:
                artist_header += f" (*{years[0]})"
        
        artist_header += "**"
        
        # Language-aware introduction
        biography_template = get_response_template(user_language, 'biography')
        message = f"{artist_header}\n\n"
        message += f"{biography_template}\n\n"
          # Create summary from Wikipedia content
        if wiki_data.get('extract'):
            summary = summarize_artist_biography(wiki_data['extract'], artist_name)
            if summary:
                message += f"{summary}\n\n"
        
        # Source information
        if wiki_data:
            language = wiki_data.get('language', 'unbekannt' if user_language == 'de' else 'unknown')
            info_source_template = get_response_template(user_language, 'info_source')
            message += f"\n{info_source_template.format(language=language)}"
        
        dispatcher.utter_message(text=message)
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        user_language = detect_user_language(user_message)
        
        artist_name_slot = tracker.get_slot("artist_name")
        # Renamed for clarity
        artist_name_intent_extracted = extract_artist_from_message(user_message)

        logger.debug(f"Artist slot: '{artist_name_slot}', Artist from message extraction: '{artist_name_intent_extracted}'")

        chosen_artist_name = None
        if artist_name_slot and artist_name_intent_extracted:
            # Prefer intent_extracted if it's a known full name and slot is its mapped short name
            slot_lower = artist_name_slot.lower()
            if KNOWN_ARTISTS.get(slot_lower) == artist_name_intent_extracted and \
               len(artist_name_intent_extracted) > len(artist_name_slot):
                chosen_artist_name = artist_name_intent_extracted
                logger.info(f"Prioritizing mapped name from message extraction ('{artist_name_intent_extracted}') over slot ('{artist_name_slot}').")
            # Prefer intent_extracted if it's significantly longer and seems more specific (e.g. slot "Leonardo", intent "Leonardo da Vinci")
            elif artist_name_intent_extracted.lower().startswith(slot_lower) and \
                 len(artist_name_intent_extracted) > len(artist_name_slot) + 3: # Arbitrary length diff, e.g. "da Vinci" is +8
                chosen_artist_name = artist_name_intent_extracted
                logger.info(f"Prioritizing longer name from message extraction ('{artist_name_intent_extracted}') over slot ('{artist_name_slot}').")
            # Fallback to slot if intent is not clearly better or if they are very similar
            else:
                chosen_artist_name = artist_name_slot
                logger.info(f"Using slot name ('{artist_name_slot}') as message extraction ('{artist_name_intent_extracted}') was not deemed significantly more specific.")
        elif artist_name_slot:
            chosen_artist_name = artist_name_slot
        elif artist_name_intent_extracted:
            chosen_artist_name = artist_name_intent_extracted
        
        if not chosen_artist_name:
            no_artist_template = get_response_template(user_language, 'no_artist_specified')
            dispatcher.utter_message(text=no_artist_template)
            logger.debug("No artist name found in slot or message extraction.")
            return []
        
        artist_name_for_search = chosen_artist_name 
        
        logger.info(f"Selected artist name for search: '{artist_name_for_search}' (Language: {user_language})")
        
        try:
            # Clean the selected artist name before sending to Wikipedia client
            # This cleaning is mainly for removing conversational fluff or suffixes like (Maler)
            # if they were inadvertently part of the chosen_artist_name.
            # KNOWN_ARTISTS should map to canonical names without such suffixes.
            cleaned_artist_name_for_search = artist_name_for_search.replace("(Maler)", "").replace("(Künstler)", "").replace("(Artist)", "").replace("(Painter)", "").replace("(Bildhauer)", "").replace("(sculptor)", "").strip()
            if not cleaned_artist_name_for_search: # if stripping made it empty
                 cleaned_artist_name_for_search = artist_name_for_search # revert to original

            logger.info(f"Cleaned artist name for Wikipedia client: '{cleaned_artist_name_for_search}'")
            wiki_data = wikipedia_client.search_artist(cleaned_artist_name_for_search)
            
            if wiki_data and wiki_data.get('extract') and wiki_data.get('title'):
                # Use the title from Wikipedia as the display name
                display_name = wiki_data.get('title')
                self.create_artist_response(dispatcher, wiki_data, display_name, user_language)
            else:
                logger.warning(f"No sufficient Wikipedia data found for artist '{cleaned_artist_name_for_search}'. Searched for: '{artist_name_for_search}'")
                artist_not_found_template = get_response_template(user_language, 'artist_not_found')
                # Use the name we intended to search for in the "not found" message
                dispatcher.utter_message(text=artist_not_found_template.format(artist_name=artist_name_for_search))
                
        except Exception as e:
            logger.error(f"Fehler bei Künstler-Suche für '{artist_name_for_search}': {e}", exc_info=True)
            technical_error_template = get_response_template(user_language, 'technical_error')
            dispatcher.utter_message(text=technical_error_template)
        
        return []
