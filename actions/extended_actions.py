"""
Erweiterte Actions für umfangreichere Chatbot-Funktionalität
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
    detect_user_language,
    get_response_template
)

logger = setup_logger(__name__)

class ActionFetchArtInfo(Action):
    """Holt Informationen über Kunstrichtungen, Techniken und Geschichte"""
    
    def name(self) -> Text:
        return "action_fetch_art_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Detect user language
        user_language = detect_user_language(tracker.latest_message.get('text', ''))
        
        # Extract relevant entities
        art_movement = tracker.get_slot('art_movement')
        art_technique = tracker.get_slot('art_technique')
        time_period = tracker.get_slot('time_period')
        
        # Determine what type of information is requested
        intent = tracker.latest_message.get('intent', {}).get('name')
        
        try:
            if intent == 'ask_art_movement' and art_movement:
                info = self._get_art_movement_info(art_movement, user_language)
            elif intent == 'ask_art_technique' and art_technique:
                info = self._get_art_technique_info(art_technique, user_language)
            elif intent == 'ask_art_history' or time_period:
                info = self._get_art_history_info(time_period, user_language)
            else:
                info = self._get_general_art_info(user_language)
            
            # Send response
            if info:
                dispatcher.utter_message(text=info)
            else:
                template = get_response_template(user_language, 'not_found')
                dispatcher.utter_message(text=template)
                
        except Exception as e:
            logger.error(f"Error in ActionFetchArtInfo: {e}")
            template = get_response_template(user_language, 'error')
            dispatcher.utter_message(text=template)
        
        return []
    
    def _get_art_movement_info(self, movement: str, language: str) -> str:
        """Informationen über Kunstrichtungen"""
        movements = {
            'impressionismus': {
                'de': "🎨 **Impressionismus**\n\nDer Impressionismus entstand in der zweiten Hälfte des 19. Jahrhunderts in Frankreich. Die Künstler malten oft im Freien und fingen das wechselnde Licht und die Atmosphäre ein. Bekannte Vertreter: Claude Monet, Auguste Renoir, Edgar Degas.",
                'en': "🎨 **Impressionism**\n\nImpressionism emerged in France in the second half of the 19th century. Artists often painted outdoors, capturing changing light and atmosphere. Famous representatives: Claude Monet, Auguste Renoir, Edgar Degas."
            },
            'kubismus': {
                'de': "🔳 **Kubismus**\n\nDer Kubismus revolutionierte die Kunst im frühen 20. Jahrhundert. Objekte wurden in geometrische Formen zerlegt und aus verschiedenen Blickwinkeln dargestellt. Begründer: Pablo Picasso und Georges Braque.",
                'en': "🔳 **Cubism**\n\nCubism revolutionized art in the early 20th century. Objects were broken down into geometric forms and shown from multiple viewpoints. Founders: Pablo Picasso and Georges Braque."
            },
            'surrealismus': {
                'de': "🌙 **Surrealismus**\n\nDer Surrealismus entstand in den 1920er Jahren und erforschte das Unterbewusstsein und Träume. Die Künstler schufen traumhafte, oft bizarre Welten. Bekannte Künstler: Salvador Dalí, René Magritte, Max Ernst.",
                'en': "🌙 **Surrealism**\n\nSurrealism emerged in the 1920s, exploring the subconscious and dreams. Artists created dreamlike, often bizarre worlds. Famous artists: Salvador Dalí, René Magritte, Max Ernst."
            }
        }
        
        movement_lower = movement.lower()
        if movement_lower in movements:
            return movements[movement_lower].get(language, movements[movement_lower]['de'])
        
        return None
    
    def _get_art_technique_info(self, technique: str, language: str) -> str:
        """Informationen über Kunsttechniken"""
        techniques = {
            'ölmalerei': {
                'de': "🎨 **Ölmalerei**\n\nEine der wichtigsten Maltechniken, bei der Pigmente in Öl gebunden werden. Ermöglicht langsames Arbeiten, Korrekturen und feine Farbübergänge. Seit dem 15. Jahrhundert die bevorzugte Technik vieler Meister.",
                'en': "🎨 **Oil Painting**\n\nOne of the most important painting techniques, where pigments are bound in oil. Allows slow work, corrections, and fine color transitions. Preferred technique of many masters since the 15th century."
            },
            'aquarell': {
                'de': "💧 **Aquarell**\n\nWasserbasierte Maltechnik mit transparenten Farben. Charakteristisch sind die fließenden Übergänge und die Leichtigkeit. Besonders beliebt für Landschaften und spontane Studien.",
                'en': "💧 **Watercolor**\n\nWater-based painting technique with transparent colors. Characterized by flowing transitions and lightness. Particularly popular for landscapes and spontaneous studies."
            },
            'tempera': {
                'de': "🥚 **Tempera**\n\nEine der ältesten Maltechniken, bei der Pigmente mit Ei oder anderen Bindemitteln gemischt werden. Trocknet schnell und ergibt leuchtende, matte Farben. Vor der Ölmalerei die wichtigste Technik.",
                'en': "🥚 **Tempera**\n\nOne of the oldest painting techniques, where pigments are mixed with egg or other binders. Dries quickly and produces bright, matte colors. The most important technique before oil painting."
            }
        }
        
        technique_lower = technique.lower()
        if technique_lower in techniques:
            return techniques[technique_lower].get(language, techniques[technique_lower]['de'])
        
        return None
    
    def _get_art_history_info(self, period: str, language: str) -> str:
        """Informationen über Kunstgeschichte"""
        periods = {
            'renaissance': {
                'de': "🏛️ **Renaissance (14.-16. Jahrhundert)**\n\nWiedergeburt der antiken Ideale. Perspektive, Anatomie und Realismus wurden perfektioniert. Große Meister: Leonardo da Vinci, Michelangelo, Raffael. Zentrum: Italien.",
                'en': "🏛️ **Renaissance (14th-16th Century)**\n\nRebirth of ancient ideals. Perspective, anatomy, and realism were perfected. Great masters: Leonardo da Vinci, Michelangelo, Raphael. Center: Italy."
            },
            'barock': {
                'de': "✨ **Barock (17.-18. Jahrhundert)**\n\nDramatische, emotionale Kunst mit starken Kontrasten. Bewegung und Theatralik stehen im Vordergrund. Wichtige Künstler: Caravaggio, Rubens, Bernini.",
                'en': "✨ **Baroque (17th-18th Century)**\n\nDramatic, emotional art with strong contrasts. Movement and theatricality are prominent. Important artists: Caravaggio, Rubens, Bernini."
            },
            '19. jahrhundert': {
                'de': "🌅 **19. Jahrhundert**\n\nZeit großer Stilrichtungen: Romantik, Realismus, Impressionismus. Akademische Tradition wird hinterfragt. Kunst wird bürgerlicher und vielfältiger.",
                'en': "🌅 **19th Century**\n\nTime of great styles: Romanticism, Realism, Impressionism. Academic tradition is questioned. Art becomes more bourgeois and diverse."
            }
        }
        
        if period:
            period_lower = period.lower()
            if period_lower in periods:
                return periods[period_lower].get(language, periods[period_lower]['de'])
        
        # General art history info if no specific period
        if language == 'en':
            return "🎨 **Art History**\n\nArt has evolved through many periods: Ancient Art, Medieval, Renaissance, Baroque, Modern Art, and Contemporary Art. Each period reflects the culture and values of its time."
        else:
            return "🎨 **Kunstgeschichte**\n\nDie Kunst hat sich durch viele Epochen entwickelt: Antike, Mittelalter, Renaissance, Barock, Moderne und Zeitgenössische Kunst. Jede Epoche spiegelt die Kultur und Werte ihrer Zeit wider."
    
    def _get_general_art_info(self, language: str) -> str:
        """Allgemeine Kunstinformationen"""
        if language == 'en':
            return "🎨 **Art Information**\n\nI can help you learn about art movements, techniques, history, and much more! What specific aspect interests you?"
        else:
            return "🎨 **Kunstinformationen**\n\nIch kann Ihnen bei Kunstrichtungen, Techniken, Geschichte und vielem mehr helfen! Welcher Aspekt interessiert Sie besonders?"


class ActionRecommendContent(Action):
    """Empfiehlt Inhalte basierend auf Kontext und Präferenzen"""
    
    def name(self) -> Text:
        return "action_recommend_content"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_language = detect_user_language(tracker.latest_message.get('text', ''))
        
        # Analyze conversation context
        last_artwork = tracker.get_slot('last_artwork')
        last_artist = tracker.get_slot('last_artist')
        art_movement = tracker.get_slot('art_movement')
        
        try:
            recommendations = self._generate_recommendations(
                last_artwork, last_artist, art_movement, user_language
            )
            
            if recommendations:
                dispatcher.utter_message(text=recommendations)
            else:
                template = self._get_general_recommendations(user_language)
                dispatcher.utter_message(text=template)
                
        except Exception as e:
            logger.error(f"Error in ActionRecommendContent: {e}")
            template = get_response_template(user_language, 'error')
            dispatcher.utter_message(text=template)
        
        return []
    
    def _generate_recommendations(self, artwork: str, artist: str, movement: str, language: str) -> str:
        """Generiert kontextbasierte Empfehlungen"""
        
        # Artist-based recommendations
        if artist:
            if 'van gogh' in artist.lower():
                if language == 'en':
                    return "💡 **Recommendations**\n\nSince you're interested in Van Gogh, you might also like:\n• Paul Cézanne - Post-Impressionist master\n• Paul Gauguin - Van Gogh's friend and colleague\n• Henri de Toulouse-Lautrec - Contemporary artist\n• Wheat Field with Cypresses - Another Van Gogh masterpiece"
                else:
                    return "💡 **Empfehlungen**\n\nDa Sie sich für Van Gogh interessieren, könnten Ihnen auch gefallen:\n• Paul Cézanne - Postimpressionistischer Meister\n• Paul Gauguin - Van Goghs Freund und Kollege\n• Henri de Toulouse-Lautrec - Zeitgenössischer Künstler\n• Weizenfeld mit Zypressen - Ein weiteres Van Gogh Meisterwerk"
            
            elif 'picasso' in artist.lower():
                if language == 'en':
                    return "💡 **Recommendations**\n\nFor Picasso enthusiasts, consider:\n• Georges Braque - Co-founder of Cubism\n• Les Demoiselles d'Avignon - Revolutionary Picasso work\n• Henri Matisse - Picasso's friendly rival\n• Cubism movement exploration"
                else:
                    return "💡 **Empfehlungen**\n\nFür Picasso-Interessierte:\n• Georges Braque - Mitbegründer des Kubismus\n• Les Demoiselles d'Avignon - Revolutionäres Picasso-Werk\n• Henri Matisse - Picassos freundschaftlicher Rivale\n• Erkundung der Kubismus-Bewegung"
        
        # Artwork-based recommendations
        if artwork:
            if 'mona lisa' in artwork.lower():
                if language == 'en':
                    return "💡 **Recommendations**\n\nIf you love the Mona Lisa:\n• Lady with an Ermine - Another Leonardo portrait\n• Girl with a Pearl Earring - Vermeer's mysterious portrait\n• Renaissance portrait painting techniques\n• Visit the Louvre Museum virtually"
                else:
                    return "💡 **Empfehlungen**\n\nWenn Ihnen die Mona Lisa gefällt:\n• Dame mit Hermelin - Ein weiteres Leonardo-Portrait\n• Mädchen mit dem Perlenohrring - Vermeers geheimnisvolles Portrait\n• Renaissance-Porträtmalerei-Techniken\n• Virtueller Besuch im Louvre Museum"
        
        # Movement-based recommendations
        if movement:
            if 'impressionismus' in movement.lower():
                if language == 'en':
                    return "💡 **Recommendations**\n\nFor Impressionism lovers:\n• Claude Monet's Water Lilies series\n• Auguste Renoir's joyful scenes\n• Edgar Degas' ballet dancers\n• Visit Musée d'Orsay in Paris"
                else:
                    return "💡 **Empfehlungen**\n\nFür Impressionismus-Liebhaber:\n• Claude Monets Seerosen-Serie\n• Auguste Renoirs fröhliche Szenen\n• Edgar Degas' Balletttänzerinnen\n• Besuch im Musée d'Orsay in Paris"
        
        return None
    
    def _get_general_recommendations(self, language: str) -> str:
        """Allgemeine Empfehlungen"""
        if language == 'en':
            return "💡 **General Recommendations**\n\nHere are some timeless masterpieces to explore:\n• Mona Lisa by Leonardo da Vinci\n• Starry Night by Vincent van Gogh\n• Guernica by Pablo Picasso\n• Girl with a Pearl Earring by Vermeer\n\nWhat type of art interests you most?"
        else:
            return "💡 **Allgemeine Empfehlungen**\n\nHier sind einige zeitlose Meisterwerke zum Erkunden:\n• Mona Lisa von Leonardo da Vinci\n• Sternennacht von Vincent van Gogh\n• Guernica von Pablo Picasso\n• Mädchen mit dem Perlenohrring von Vermeer\n\nWelche Art von Kunst interessiert Sie am meisten?"


class ActionCompareArtworks(Action):
    """Vergleicht Kunstwerke oder Künstler"""
    
    def name(self) -> Text:
        return "action_compare_artworks"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_language = detect_user_language(tracker.latest_message.get('text', ''))
        
        # Extract entities for comparison
        entities = tracker.latest_message.get('entities', [])
        artworks = [e['value'] for e in entities if e['entity'] == 'artwork_name']
        artists = [e['value'] for e in entities if e['entity'] == 'artist_name']
        
        try:
            if len(artworks) >= 2:
                comparison = self._compare_artworks(artworks[0], artworks[1], user_language)
            elif len(artists) >= 2:
                comparison = self._compare_artists(artists[0], artists[1], user_language)
            else:
                comparison = self._get_comparison_help(user_language)
            
            dispatcher.utter_message(text=comparison)
                
        except Exception as e:
            logger.error(f"Error in ActionCompareArtworks: {e}")
            template = get_response_template(user_language, 'error')
            dispatcher.utter_message(text=template)
        
        return []
    
    def _compare_artworks(self, artwork1: str, artwork2: str, language: str) -> str:
        """Vergleicht zwei Kunstwerke"""
        # Simplified comparison examples
        comparisons = {
            ('mona lisa', 'girl with a pearl earring'): {
                'de': "🎨 **Vergleich: Mona Lisa vs. Mädchen mit dem Perlenohrring**\n\n**Gemeinsamkeiten:**\n• Beide sind berühmte Frauenporträts\n• Geheimnisvolle Ausstrahlung\n• Meisterhafte Maltechnik\n\n**Unterschiede:**\n• Mona Lisa: Renaissance (da Vinci)\n• Mädchen: Barock (Vermeer)\n• Verschiedene Maltechniken und Stile",
                'en': "🎨 **Comparison: Mona Lisa vs. Girl with a Pearl Earring**\n\n**Similarities:**\n• Both are famous female portraits\n• Mysterious aura\n• Masterful painting technique\n\n**Differences:**\n• Mona Lisa: Renaissance (da Vinci)\n• Girl: Baroque (Vermeer)\n• Different painting techniques and styles"
            }
        }
        
        key = (artwork1.lower(), artwork2.lower())
        reverse_key = (artwork2.lower(), artwork1.lower())
        
        if key in comparisons:
            return comparisons[key].get(language, comparisons[key]['de'])
        elif reverse_key in comparisons:
            return comparisons[reverse_key].get(language, comparisons[reverse_key]['de'])
        
        # Generic comparison
        if language == 'en':
            return f"🎨 **Comparison: {artwork1} vs. {artwork2}**\n\nBoth are significant artworks with their own unique characteristics. Would you like me to provide specific information about each work individually?"
        else:
            return f"🎨 **Vergleich: {artwork1} vs. {artwork2}**\n\nBeide sind bedeutende Kunstwerke mit ihren eigenen einzigartigen Eigenschaften. Möchten Sie, dass ich spezifische Informationen zu jedem Werk einzeln gebe?"
    
    def _compare_artists(self, artist1: str, artist2: str, language: str) -> str:
        """Vergleicht zwei Künstler"""
        # Simplified artist comparisons
        if language == 'en':
            return f"👥 **Artist Comparison: {artist1} vs. {artist2}**\n\nBoth artists have made unique contributions to art history. Each developed their own distinctive style and techniques. Would you like specific information about their artistic movements or techniques?"
        else:
            return f"👥 **Künstler-Vergleich: {artist1} vs. {artist2}**\n\nBeide Künstler haben einzigartige Beiträge zur Kunstgeschichte geleistet. Jeder entwickelte seinen eigenen unverwechselbaren Stil und Techniken. Möchten Sie spezifische Informationen über ihre Kunstrichtungen oder Techniken?"
    
    def _get_comparison_help(self, language: str) -> str:
        """Hilfe für Vergleiche"""
        if language == 'en':
            return "🔍 **Comparison Help**\n\nI can compare artworks or artists for you! Try asking:\n• 'Compare Mona Lisa and Girl with a Pearl Earring'\n• 'Difference between Monet and Manet'\n• 'Van Gogh vs Picasso'"
        else:
            return "🔍 **Vergleichs-Hilfe**\n\nIch kann Kunstwerke oder Künstler für Sie vergleichen! Versuchen Sie:\n• 'Vergleiche Mona Lisa und Mädchen mit dem Perlenohrring'\n• 'Unterschied zwischen Monet und Manet'\n• 'Van Gogh vs Picasso'"


class ActionSaveUserPreference(Action):
    """Speichert Nutzerpräferenzen für personalisierte Empfehlungen"""
    
    def name(self) -> Text:
        return "action_save_user_preference"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract preferences from conversation
        # This is a simplified implementation
        return []
