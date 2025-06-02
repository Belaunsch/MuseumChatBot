"""
Greeting and farewell actions for the Museum Chatbot
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


class ActionGreet(Action):
    """Greets the user"""
    
    def name(self) -> Text:
        return "action_greet"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        user_language = detect_user_language(user_message)
        
        if user_language == 'en':
            message = ("🎨 **Welcome to the Museum Chatbot!**\n\n"
                      "I'm your personal guide through the fascinating world of art. "
                      "I can help you discover amazing artworks and learn about famous artists.\n\n"
                      "**Examples:** *\"Tell me about the Mona Lisa\"* or *\"Who was Van Gogh?\"*\n\n"
                      "Which artwork or artist interests you?")
        else:
            message = ("🎨 **Willkommen beim Museum-Chatbot!**\n\n"
                      "Ich bin Ihr persönlicher Führer durch die faszinierende Welt der Kunst. "
                      "Gerne helfe ich Ihnen dabei, erstaunliche Kunstwerke zu entdecken und berühmte Künstler kennenzulernen.\n\n"
                      "**Beispiele:** *\"Erzähl mir über die Mona Lisa\"* oder *\"Wer war Van Gogh?\"*\n\n"
                      "Welches Kunstwerk oder welcher Künstler interessiert Sie?")
        
        dispatcher.utter_message(text=message)
        return []


class ActionGoodbye(Action):
    """Says goodbye to the user"""
    
    def name(self) -> Text:
        return "action_goodbye"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        user_language = detect_user_language(user_message)
        
        if user_language == 'en':
            message = ("🎨 **Thank you for your visit!**\n\n"
                      "I hope I could inspire you with fascinating insights into the world of art. "
                      "Feel free to come back anytime to discover more artworks and artists!\n\n"
                      "Have a wonderful day! 🌟")
        else:
            message = ("🎨 **Vielen Dank für Ihren Besuch!**\n\n"
                      "Ich hoffe, ich konnte Sie mit faszinierenden Einblicken in die Welt der Kunst begeistern. "
                      "Kommen Sie gerne jederzeit zurück, um weitere Kunstwerke und Künstler zu entdecken!\n\n"
                      "Haben Sie einen wunderbaren Tag! 🌟")
        
        dispatcher.utter_message(text=message)
        return []
