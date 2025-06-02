"""
Museum information actions for the Museum Chatbot
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

from utils import setup_logger, detect_user_language

logger = setup_logger(__name__)


class ActionFetchMuseumInfo(Action):
    """Searches for museum information"""
    
    def name(self) -> Text:
        return "action_fetch_museum_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        user_language = detect_user_language(user_message)
        
        if user_language == 'en':
            message = ("🏛️ **Museum Information**\n\n"
                      "This feature is currently being updated to provide you with the best "
                      "and most current museum information.\n\n"
                      "In the meantime, I'd be happy to help you with questions about "
                      "**artworks** and **artists**!")
        else:
            message = ("🏛️ **Museum-Informationen**\n\n"
                      "Diese Funktion wird derzeit überarbeitet, um Ihnen die besten "
                      "und aktuellsten Museum-Informationen zu liefern.\n\n"
                      "In der Zwischenzeit kann ich Ihnen gerne bei Fragen zu "
                      "**Kunstwerken** und **Künstlern** weiterhelfen!")
        
        dispatcher.utter_message(text=message)
        return []
