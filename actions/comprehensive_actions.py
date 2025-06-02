"""
Erweiterte Actions für umfangreicheres Training des MuseumChatBots
Behandelt neue Intents wie Kunstrichtungen, Techniken, Vergleiche und Empfehlungen
"""
import os
import sys
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Add utils to path
utils_path = os.path.join(os.path.dirname(__file__), 'utils')
if utils_path not in sys.path:
    sys.path.insert(0, utils_path)

from utils import (
    setup_logger,
    wikipedia_client,
    summarize_wikipedia_content,
    detect_user_language,
    get_response_template
)

logger = setup_logger(__name__)


class ActionFetchArtInfo(Action):
    """Behandelt Kunstrichtungen, Techniken und Kunstgeschichte"""
    
    def name(self) -> Text:
        return "action_fetch_art_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Extrahiere relevante Entities
            art_movement_slot = tracker.get_slot("art_movement")
            art_technique_slot = tracker.get_slot("art_technique")
            time_period_slot = tracker.get_slot("time_period")
            latest_message_text = tracker.latest_message.get('text', '').lower()
            
            search_term = None
            category = None
            
            # Prioritize slots
            if art_movement_slot:
                search_term = art_movement_slot
                category = "Kunstrichtung"
            elif art_technique_slot:
                search_term = art_technique_slot
                category = "Kunsttechnik"
            elif time_period_slot:
                search_term = f"Kunst {time_period_slot}" # Consider if "Kunst " prefix is always best
                category = "Kunstgeschichte"
            else:
                # Fallback: More robust keyword extraction from the latest message
                art_keywords_map = {
                    "impressionismus": "Impressionismus",
                    "kubismus": "Kubismus",
                    "surrealismus": "Surrealismus",
                    "expressionismus": "Expressionismus",
                    "pop art": "Pop Art", # Multi-word
                    "popart": "Pop Art",
                    "renaissance": "Renaissance",
                    "barock": "Barock",
                    "moderne kunst": "Moderne Kunst",
                    "abstrakte kunst": "Abstrakte Kunst",
                    "romantik": "Romantik", # Ensure these match NLU examples if possible
                    "realismus": "Realismus",
                    "fauvismus": "Fauvismus",
                    "dadaismus": "Dadaismus",
                    "klassizismus": "Klassizismus"
                }
                technique_keywords_map = {
                    "ölmalerei": "Ölmalerei",
                    "aquarell": "Aquarell",
                    "tempera": "Tempera",
                    "radierung": "Radierung",
                    "skulptur": "Skulptur"
                }

                for keyword, term_value in art_keywords_map.items():
                    if keyword in latest_message_text:
                        search_term = term_value
                        category = "Kunstrichtung"
                        break
                
                if not search_term:
                    for keyword, term_value in technique_keywords_map.items():
                        if keyword in latest_message_text:
                            search_term = term_value
                            category = "Kunsttechnik"
                            break
                
                # If still no specific term extracted, and it's likely an art movement question
                if not search_term and tracker.latest_message.get('intent', {}).get('name') == 'ask_art_movement':
                    # Try to be a bit smarter: extract nouns or proper nouns?
                    # For now, if intent is ask_art_movement but no keyword found, ask for clarification.
                    # This avoids searching Wikipedia with a full vague question like "Was zeichnet XY aus?"
                    # which might have been misclassified or where XY is unknown.
                    # However, the original user query "Was ist Impressionismus?" should have "Impressionismus"
                    # extracted by the NLU into the art_movement_slot ideally.
                    # This fallback is more for when the slot is empty AND simple keyword search fails.
                    
                    # If the original query was "Was zeichnet den Barock aus?", NLU might provide "Barock" in slot.
                    # If not, "barock" keyword search above should catch it.
                    # This part is a safety net.
                    # If the original message was "Was ist Kunst?" - this is too broad.
                    # Let's attempt to use the original latest_message_text if it's short and seems like a term
                    potential_term = tracker.latest_message.get('text', '')
                    if len(potential_term.split()) <= 3: # Arbitrary short phrase
                         # Attempt to clean it up slightly (e.g. remove "Was ist", "Erzähl mir über")
                        phrases_to_remove = ["was ist ", "erkläre mir ", "erzähl mir über ", "was bedeutet ", " kunst", " in der kunst"]
                        cleaned_term = potential_term.lower()
                        for phrase in phrases_to_remove:
                            cleaned_term = cleaned_term.replace(phrase, "")
                        cleaned_term = cleaned_term.strip().title() # Capitalize for Wikipedia
                        if cleaned_term:
                            search_term = cleaned_term
                            # Best guess for category, or leave it generic "Kunst"
                            category = "Kunstthema" # Generic category
                        else: # If cleaning results in empty, ask
                            dispatcher.utter_message(template="utter_ask_specific_art_topic") # A new response needed in domain
                            return [SlotSet("art_movement", None)] # Clear slot if it was wrongly filled
                    else:
                         dispatcher.utter_message(template="utter_ask_specific_art_topic")
                         return [SlotSet("art_movement", None)]


            if not search_term:
                # If after all logic, search_term is still None, ask for clarification.
                # This replaces the previous: dispatcher.utter_message(text="Zu welchem Kunstthema möchten Sie mehr erfahren?")
                dispatcher.utter_message(template="utter_ask_specific_art_topic") # Ensure this response is in domain.yml
                return []
            
            logger.info(f"Suche Kunstinformationen für: '{search_term}' (Kategorie: {category or 'Unbekannt'})")
            
            # Suche in Wikipedia
            # Ensure wikipedia_client is initialized (assuming it is from utils)
            page = None
            try:
                page = wikipedia_client.page(search_term) # Search with the cleaner term
            except Exception as wiki_error: # Catch specific wikipedia exceptions if possible
                logger.error(f"Wikipedia search error for '{search_term}': {wiki_error}")
            
            if page and page.exists(): # Check if page actually exists
                content = summarize_wikipedia_content(page.summary, max_sentences=5) # Use summary, often cleaner
                
                if not content.strip(): # If summary is empty or just whitespace
                    content = summarize_wikipedia_content(page.content, max_sentences=5) # Fallback to full content

                if not content.strip(): # If still no content
                    dispatcher.utter_message(text=f"Ich habe einen Artikel zu '{page.title}' gefunden, konnte aber keine Zusammenfassung erstellen. Möchten Sie den Link zur Seite? {page.fullurl}")
                    return [SlotSet("last_query", search_term), SlotSet("conversation_context", category)]

                # Formatierte Antwort
                title = page.title
                if category:
                    response_text = f"🎨 **{category}: {title}**\\n\\n"
                else:
                    response_text = f"🎨 **{title}**\\n\\n"

                response_text += f"📖 **Information (Quelle: Wikipedia):**\\n{content}\\n\\n"
                response_text += f"🔗 Mehr dazu: {page.fullurl}\\n\\n"
                
                # Zusätzliche Empfehlungen je nach Kategorie
                if category == "Kunstrichtung" and (art_movement_slot or search_term.lower() in art_keywords_map): # Check if it was indeed an art movement
                    response_text += "💡 **Tipp:** Fragen Sie mich nach berühmten Künstlern oder Werken dieser Richtung!"
                elif category == "Kunsttechnik" and (art_technique_slot or search_term.lower() in technique_keywords_map):
                    response_text += "💡 **Tipp:** Ich kann Ihnen Kunstwerke zeigen, die in dieser Technik erstellt wurden!"
                
                dispatcher.utter_message(text=response_text)
                
                return [
                    SlotSet("last_query", search_term),
                    SlotSet("art_movement", search_term if category == "Kunstrichtung" else None), # Update slot if we deduced it
                    SlotSet("conversation_context", category)
                ]
            else:
                # If page doesn't exist or search_term was too vague.
                # Check if the original intent was 'ask_art_movement'
                if tracker.latest_message.get('intent', {}).get('name') == 'ask_art_movement':
                     dispatcher.utter_message(text=f"Ich konnte leider keine spezifischen Informationen zur Kunstrichtung '{search_term}' finden. Vielleicht können Sie es genauer formulieren oder eine andere bekannte Kunstrichtung nennen?")
                else:
                    dispatcher.utter_message(text=f"Leider konnte ich keine Informationen zu '{search_term}' finden. Versuchen Sie es mit einem anderen Begriff oder stellen Sie Ihre Frage anders.")
                return [SlotSet("art_movement", None)] # Clear slot as info not found
                
        except Exception as e:
            logger.error(f"Fehler in ActionFetchArtInfo: {e}", exc_info=True)
            dispatcher.utter_message(text="Entschuldigung, es gab einen internen Fehler beim Abrufen der Kunstinformationen. Bitte versuchen Sie es später erneut.")
            return []


class ActionRecommendContent(Action):
    """Bietet kontextbasierte Empfehlungen"""
    
    def name(self) -> Text:
        return "action_recommend_content"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Hole Kontext aus vorherigen Slots
            last_artwork = tracker.get_slot("last_artwork") or tracker.get_slot("artwork_name")
            last_artist = tracker.get_slot("last_artist") or tracker.get_slot("artist_name")
            art_movement = tracker.get_slot("art_movement")
            conversation_context = tracker.get_slot("conversation_context")
            
            recommendations = []
            
            # Empfehlungen basierend auf letztem Künstler
            if last_artist:
                if "van gogh" in last_artist.lower():
                    recommendations = [
                        "🎨 **Paul Cézanne** - Ein weiterer Post-Impressionist",
                        "🎨 **Paul Gauguin** - Van Goghs Zeitgenosse",
                        "🎨 **Henri de Toulouse-Lautrec** - Ähnliche Periode"
                    ]
                elif "picasso" in last_artist.lower():
                    recommendations = [
                        "🎨 **Georges Braque** - Mitbegründer des Kubismus",
                        "🎨 **Henri Matisse** - Zeitgenosse Picassos",
                        "🎨 **Juan Gris** - Kubistischer Maler"
                    ]
                elif "monet" in last_artist.lower():
                    recommendations = [
                        "🎨 **Pierre-Auguste Renoir** - Impressionist",
                        "🎨 **Edgar Degas** - Impressionistische Bewegung",
                        "🎨 **Camille Pissarro** - Impressionismus"
                    ]
            
            # Empfehlungen basierend auf Kunstrichtung
            elif art_movement:
                if "impressionismus" in art_movement.lower():
                    recommendations = [
                        "🖼️ **Water Lilies** von Claude Monet",
                        "🖼️ **Luncheon of the Boating Party** von Renoir",
                        "🖼️ **The Dance Class** von Edgar Degas"
                    ]
                elif "kubismus" in art_movement.lower():
                    recommendations = [
                        "🖼️ **Les Demoiselles d'Avignon** von Picasso",
                        "🖼️ **Guernica** von Picasso",
                        "🖼️ **Violin and Candlestick** von Georges Braque"
                    ]
            
            # Allgemeine Empfehlungen wenn kein spezifischer Kontext
            if not recommendations:
                recommendations = [
                    "🎨 **Vincent van Gogh** - Faszinierende Lebensgeschichte",
                    "🖼️ **The Starry Night** - Eines der berühmtesten Gemälde",
                    "🏛️ **Louvre Museum** - Mit der weltberühmten Mona Lisa",
                    "🎨 **Impressionismus** - Revolutionäre Kunstbewegung"
                ]
            
            response = "🌟 **Empfehlungen für Sie:**\n\n"
            response += "\n".join(recommendations)
            response += "\n\n💡 **Fragen Sie mich einfach nach einem der Themen!**"
            
            dispatcher.utter_message(text=response)
            return []
            
        except Exception as e:
            logger.error(f"Fehler in ActionRecommendContent: {e}")
            dispatcher.utter_message(text="Gerne gebe ich Ihnen Empfehlungen! Fragen Sie mich nach Kunstwerken, Künstlern oder Kunstrichtungen.")
            return []


class ActionCompareArtworks(Action):
    """Vergleicht Kunstwerke oder Künstler"""
    
    def name(self) -> Text:
        return "action_compare_artworks"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            latest_message = tracker.latest_message.get('text', '').lower()
            
            # Vordefinierte Vergleiche
            comparisons = {
                "monet_manet": {
                    "title": "Claude Monet vs. Édouard Manet",
                    "content": """
🎨 **Claude Monet (1840-1926)**
• Impressionist
• Bekannt für Seerosenbilder und Landschaften
• Malte oft im Freien (Plein Air)
• Fasziniert von Licht und Farbe

🎨 **Édouard Manet (1832-1883)**
• Vorläufer des Impressionismus
• Realistische Darstellungen
• Inspirierte die Impressionisten
• Bekannt für "Das Frühstück im Grünen"
                    """
                },
                "van_gogh_gauguin": {
                    "title": "Vincent van Gogh vs. Paul Gauguin",
                    "content": """
🎨 **Vincent van Gogh (1853-1890)**
• Post-Impressionist
• Expressiver, emotionaler Stil
• Dicke Farbschichten (Impasto)
• Bekannt für "Sternennacht"

🎨 **Paul Gauguin (1848-1903)**
• Post-Impressionist
• Synthetismus und Primitivismus
• Flache Farbflächen
• Lebte in der Südsee
                    """
                },
                "picasso_braque": {
                    "title": "Pablo Picasso vs. Georges Braque",
                    "content": """
🎨 **Pablo Picasso (1881-1973)**
• Mitbegründer des Kubismus
• Vielseitiger Künstler (Malerei, Skulptur)
• Verschiedene Schaffensperioden
• Bekannt für "Guernica"

🎨 **Georges Braque (1882-1963)**
• Mitbegründer des Kubismus
• Fokus auf analytischen Kubismus
• Subtilere Farbpalette
• Enge Zusammenarbeit mit Picasso
                    """
                }
            }
            
            # Erkenne Vergleichstyp
            comparison_key = None
            if any(name in latest_message for name in ["monet", "manet"]):
                comparison_key = "monet_manet"
            elif any(name in latest_message for name in ["van gogh", "gauguin"]):
                comparison_key = "van_gogh_gauguin"
            elif any(name in latest_message for name in ["picasso", "braque"]):
                comparison_key = "picasso_braque"
            
            if comparison_key and comparison_key in comparisons:
                comp = comparisons[comparison_key]
                response = f"🔍 **Vergleich: {comp['title']}**\n\n{comp['content']}\n\n💡 **Möchten Sie mehr über einen der Künstler erfahren?**"
                dispatcher.utter_message(text=response)
            else:
                # Allgemeine Vergleichshilfe
                response = """
🔍 **Kunstvergleiche**

Ich kann Ihnen bei Vergleichen helfen zwischen:
• **Künstlern**: Monet vs. Manet, Van Gogh vs. Gauguin
• **Kunstrichtungen**: Impressionismus vs. Expressionismus
• **Epochen**: Renaissance vs. Barock

**Fragen Sie mich einfach:** "Was ist der Unterschied zwischen...?"
                """
                dispatcher.utter_message(text=response)
            
            return []
            
        except Exception as e:
            logger.error(f"Fehler in ActionCompareArtworks: {e}")
            dispatcher.utter_message(text="Gerne helfe ich Ihnen bei Vergleichen! Fragen Sie mich nach Unterschieden zwischen Künstlern oder Kunstrichtungen.")
            return []


class ActionSaveUserPreference(Action):
    """Speichert Nutzerpräferenzen für personalisierte Empfehlungen"""
    
    def name(self) -> Text:
        return "action_save_user_preference"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Analysiere Nutzerverhalten aus Intent-Historie
            events = tracker.events
            preferences = []
            
            # Zähle häufig angefragte Künstler
            artist_requests = {}
            artwork_requests = {}
            
            for event in events:
                if event.get('event') == 'user' and event.get('parse_data'):
                    entities = event['parse_data'].get('entities', [])
                    for entity in entities:
                        if entity['entity'] == 'artist_name':
                            artist = entity['value']
                            artist_requests[artist] = artist_requests.get(artist, 0) + 1
                        elif entity['entity'] == 'artwork_name':
                            artwork = entity['value']
                            artwork_requests[artwork] = artwork_requests.get(artwork, 0) + 1
            
            # Bestimme Präferenzen
            if artist_requests:
                top_artist = max(artist_requests, key=artist_requests.get)
                preferences.append(f"Interessiert sich für {top_artist}")
            
            if artwork_requests:
                top_artwork = max(artwork_requests, key=artwork_requests.get)
                preferences.append(f"Fragt oft nach {top_artwork}")
            
            # Speichere Präferenzen (hier vereinfacht als Slot)
            preference_text = "; ".join(preferences) if preferences else "Allgemeine Kunstinteressen"
            
            return [SlotSet("user_preference", preference_text)]
            
        except Exception as e:
            logger.error(f"Fehler in ActionSaveUserPreference: {e}")
            return []


class ActionHandleComplexQuery(Action):
    """Behandelt komplexe, mehrschichtige Anfragen"""
    
    def name(self) -> Text:
        return "action_handle_complex_query"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            latest_message = tracker.latest_message.get('text', '').lower()
            
            # Erkenne komplexe Anfrage-Typen
            if any(word in latest_message for word in ['unterschied', 'vergleich', 'vs', 'oder']):
                # Weiterleitung an Vergleichsaction
                return [{"action": "action_compare_artworks"}]
            
            elif any(word in latest_message for word in ['empfehlung', 'vorschlag', 'ähnlich']):
                # Weiterleitung an Empfehlungsaction
                return [{"action": "action_recommend_content"}]
            
            elif any(word in latest_message for word in ['geschichte', 'entstehung', 'entwicklung']):
                # Weiterleitung an Kunstgeschichte
                return [{"action": "action_fetch_art_info"}]
            
            else:
                # Standardbehandlung
                dispatcher.utter_message(text="Das ist eine interessante Frage! Können Sie sie etwas spezifischer stellen?")
                return []
                
        except Exception as e:
            logger.error(f"Fehler in ActionHandleComplexQuery: {e}")
            dispatcher.utter_message(text="Entschuldigung, ich bin mir nicht sicher, wie ich Ihnen am besten helfen kann. Können Sie Ihre Frage anders formulieren?")
            return []
