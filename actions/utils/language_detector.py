# filepath: b:\CursorWorkspace\MuseumChatBotv2\actions\utils\language_detector.py
"""
Language detection utility for Museum Chatbot
Detects German vs English in user messages for language-aware responses
"""
import re
from typing import Dict, List
from .logging_config import setup_logger

logger = setup_logger(__name__)

class LanguageDetector:
    """Detects language in user messages with focus on German/English"""
    
    def __init__(self):
        # German indicators - words and patterns that strongly suggest German
        self.german_indicators = {
            'common_words': [
                'und', 'oder', 'aber', 'mit', 'von', 'zu', 'für', 'auf', 'in', 'an', 
                'bei', 'über', 'unter', 'durch', 'gegen', 'ohne', 'um', 'nach', 'vor',
                'ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr', 'sie',
                'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einer', 'einem',
                'ist', 'sind', 'war', 'waren', 'haben', 'hat', 'hatte', 'werden', 'wird',
                'kann', 'könnte', 'muss', 'soll', 'will', 'würde', 'möchte'
            ],
            'questions': [
                'was', 'wer', 'wie', 'wo', 'wann', 'warum', 'welche', 'welcher', 'welches'
            ],
            'art_terms': [
                'gemälde', 'kunstwerk', 'künstler', 'maler', 'malerei', 'skulptur',
                'museum', 'ausstellung', 'galerie', 'bild', 'werk'
            ],
            'patterns': [
                r'\b\w+en\b',  # -en endings (common in German verbs/nouns)
                r'\b\w+ung\b',  # -ung endings
                r'\b\w+keit\b',  # -keit endings
                r'\b\w+heit\b',  # -heit endings
                r'\bge\w+\b',  # ge- prefix
            ]
        }
        
        # English indicators
        self.english_indicators = {
            'common_words': [
                'and', 'or', 'but', 'with', 'from', 'to', 'for', 'on', 'in', 'at',
                'by', 'about', 'under', 'through', 'against', 'without', 'around', 'after', 'before',
                'i', 'you', 'he', 'she', 'it', 'we', 'they',
                'the', 'a', 'an', 'this', 'that', 'these', 'those',
                'is', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would',
                'can', 'could', 'must', 'should', 'want', 'need'
            ],
            'questions': [
                'what', 'who', 'how', 'where', 'when', 'why', 'which'
            ],
            'art_terms': [
                'painting', 'artwork', 'artist', 'painter', 'sculpture',
                'museum', 'exhibition', 'gallery', 'picture', 'work'
            ],
            'patterns': [
                r'\b\w+ing\b',  # -ing endings
                r'\b\w+ed\b',   # -ed endings
                r'\b\w+ly\b',   # -ly endings
                r'\b\w+tion\b', # -tion endings
            ]
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detects language of the input text
        
        Args:
            text: Input text to analyze
            
        Returns:
            'de' for German, 'en' for English
        """
        if not text or not text.strip():
            return 'de'  # Default to German
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        if not words:
            return 'de'
        
        german_score = self._calculate_language_score(text_lower, words, 'de')
        english_score = self._calculate_language_score(text_lower, words, 'en')
        
        logger.info(f"Language detection - German: {german_score}, English: {english_score}")
        
        # If scores are very close, use additional heuristics
        if abs(german_score - english_score) < 0.1:
            return self._use_heuristics(text_lower, words)
        
        return 'de' if german_score > english_score else 'en'
    
    def _calculate_language_score(self, text: str, words: List[str], language: str) -> float:
        """Calculate language score based on indicators"""
        indicators = self.german_indicators if language == 'de' else self.english_indicators
        score = 0.0
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        # Common words (high weight)
        common_word_matches = sum(1 for word in words if word in indicators['common_words'])
        score += (common_word_matches / total_words) * 0.4
        
        # Question words (medium weight)
        question_matches = sum(1 for word in words if word in indicators['questions'])
        score += (question_matches / total_words) * 0.3
        
        # Art-specific terms (medium weight)
        art_matches = sum(1 for word in words if word in indicators['art_terms'])
        score += (art_matches / total_words) * 0.2
        
        # Pattern matches (lower weight)
        pattern_matches = 0
        for pattern in indicators['patterns']:
            pattern_matches += len(re.findall(pattern, text))
        score += min(pattern_matches / total_words, 0.3) * 0.1
        
        return score
    
    def _use_heuristics(self, text: str, words: List[str]) -> str:
        """Additional heuristics when scores are close"""
        
        # Check for definitive German patterns
        german_definitive = [
            r'\bist\s+ein\b', r'\bist\s+eine\b', r'\bist\s+das\b',
            r'\bzeig\w*\s+mir\b', r'\berzähl\w*\s+mir\b',
            r'\bwas\s+ist\b', r'\bwer\s+ist\b', r'\bwie\s+ist\b'
        ]
        
        for pattern in german_definitive:
            if re.search(pattern, text):
                logger.info(f"German heuristic match: {pattern}")
                return 'de'
        
        # Check for definitive English patterns
        english_definitive = [
            r'\bwhat\s+is\b', r'\bwho\s+is\b', r'\bhow\s+is\b',
            r'\btell\s+me\s+about\b', r'\bshow\s+me\b',
            r'\bi\s+want\s+to\s+know\b'
        ]
        
        for pattern in english_definitive:
            if re.search(pattern, text):
                logger.info(f"English heuristic match: {pattern}")
                return 'en'
        
        # Default to German for ambiguous cases
        return 'de'

# Response templates for different languages
RESPONSE_TEMPLATES = {
    'de': {
        'artwork_not_found': (
            "🎨 Entschuldigung, ich konnte leider keine verlässlichen Informationen "
            "zum Kunstwerk **\"{artwork_name}\"** finden.\n\n"
            "💡 **Tipp:** Versuchen Sie es mit dem vollständigen Namen des Kunstwerks "
            "oder einem bekannteren Titel. Zum Beispiel:\n"
            "• \"Mona Lisa\"\n"
            "• \"The Starry Night\"\n"
            "• \"Guernica\"\n"
            "• \"Girl with a Pearl Earring\""
        ),
        'artist_not_found': (
            "👨‍🎨 Entschuldigung, ich konnte keine Informationen zum Künstler **\"{artist_name}\"** finden.\n\n"
            "💡 **Tipp:** Überprüfen Sie die Schreibweise oder versuchen Sie es mit dem vollständigen Namen."
        ),
        'technical_error': (
            "🎨 Entschuldigung, bei der Suche ist ein technischer Fehler aufgetreten. "
            "Bitte versuchen Sie es in einem Moment erneut."
        ),
        'no_artwork_specified': (
            "Bitte geben Sie den Namen eines Kunstwerks an, über das Sie mehr erfahren möchten."
        ),
        'no_artist_specified': (
            "Bitte geben Sie den Namen eines Künstlers an, über den Sie mehr erfahren möchten."
        ),        'artwork_intro': "Das wundervolle Werk **\"{title}\"** wurde von **{artist}**",
        'artwork_created': "geschaffen.",
        'about_artwork': "📖 **Über das Kunstwerk:**",
        'did_you_know': "💡 **Wussten Sie schon?**",
        'artist_label': "👨‍🎨 **Künstler:**",
        'biography': "📖 **Biographie:**",
        'learn_more': "🔗 **Mehr erfahren:**",
        'remarkable_artwork': "Dieses bemerkenswerte Kunstwerk stammt von **{artist}**."
    },
    'en': {
        'artwork_not_found': (
            "🎨 Sorry, I couldn't find reliable information "
            "about the artwork **\"{artwork_name}\"**.\n\n"
            "💡 **Tip:** Try using the full name of the artwork "
            "or a more well-known title. For example:\n"
            "• \"Mona Lisa\"\n"
            "• \"The Starry Night\"\n"
            "• \"Guernica\"\n"
            "• \"Girl with a Pearl Earring\""
        ),
        'artist_not_found': (
            "👨‍🎨 Sorry, I couldn't find information about the artist **\"{artist_name}\"**.\n\n"
            "💡 **Tip:** Check the spelling or try using the full name."
        ),
        'technical_error': (
            "🎨 Sorry, a technical error occurred during the search. "
            "Please try again in a moment."
        ),
        'no_artwork_specified': (
            "Please specify the name of an artwork you'd like to learn more about."
        ),
        'no_artist_specified': (
            "Please specify the name of an artist you'd like to learn more about."
        ),
        'artwork_intro': "The wonderful work **\"{title}\"** was created by **{artist}**",        'artwork_created': ".",
        'about_artwork': "📖 **About the artwork:**",
        'did_you_know': "💡 **Did you know?**",
        'artist_label': "👨‍🎨 **Artist:**",
        'biography': "📖 **Biography:**",
        'learn_more': "🔗 **Learn more:**",
        'remarkable_artwork': "This remarkable artwork was created by **{artist}**."
    }
}

# Global instance
language_detector = LanguageDetector()

def detect_user_language(text: str) -> str:
    """
    Detect the language of user input
    
    Args:
        text: User input text
        
    Returns:
        'de' for German, 'en' for English
    """
    return language_detector.detect_language(text)

def get_response_template(language: str, template_key: str) -> str:
    """
    Get response template for specific language
    
    Args:
        language: 'de' or 'en'
        template_key: Key for the template
        
    Returns:
        Template string
    """
    templates = RESPONSE_TEMPLATES.get(language, RESPONSE_TEMPLATES['de'])
    return templates.get(template_key, "")