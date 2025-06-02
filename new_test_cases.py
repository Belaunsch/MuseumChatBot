#!/usr/bin/env python3
"""
Neue Testfälle für den Museum Guide Chatbot
Erweiterte Sammlung von Testfällen basierend auf spezifischen Kategorien
"""

from typing import List, Dict, Any


class NewTestCaseProvider:
    """Sammlung aller neuen Testfälle organisiert nach Kategorien"""
    
    @staticmethod
    def greeting_tests() -> List[Dict[str, Any]]:
        """Begrüßung Tests (5 tests)"""
        return [
            {
                "id": 101,
                "category": "greeting",
                "description": "Simple greeting",
                "input": "Hallo!",
                "expected_intent": "greet"
            },
            {
                "id": 102,
                "category": "greeting",
                "description": "Casual greeting with question",
                "input": "Hi, wie geht's?",
                "expected_intent": "greet"
            },
            {
                "id": 103,
                "category": "greeting",
                "description": "Formal greeting",
                "input": "Guten Tag!",
                "expected_intent": "greet"
            },
            {
                "id": 104,
                "category": "greeting",
                "description": "Casual greeting with slang",
                "input": "Hey, was läuft?",
                "expected_intent": "greet"
            },
            {
                "id": 105,
                "category": "greeting",
                "description": "Regional greeting",
                "input": "Servus, ich bin da.",
                "expected_intent": "greet"
            }
        ]
    
    @staticmethod
    def farewell_tests() -> List[Dict[str, Any]]:
        """Verabschiedung Tests (5 tests)"""
        return [
            {
                "id": 106,
                "category": "farewell",
                "description": "Simple goodbye",
                "input": "Tschüss!",
                "expected_intent": "goodbye"
            },
            {
                "id": 107,
                "category": "farewell",
                "description": "See you soon",
                "input": "Bis bald!",
                "expected_intent": "goodbye"
            },
            {
                "id": 108,
                "category": "farewell",
                "description": "Thank you and goodbye",
                "input": "Vielen Dank, mach's gut!",
                "expected_intent": "goodbye"
            },
            {
                "id": 109,
                "category": "farewell",
                "description": "Formal goodbye",
                "input": "Auf Wiedersehen.",
                "expected_intent": "goodbye"
            },
            {
                "id": 110,
                "category": "farewell",
                "description": "Casual leaving",
                "input": "Ok, ich muss los.",
                "expected_intent": "goodbye"
            }
        ]
    
    @staticmethod
    def artwork_info_tests() -> List[Dict[str, Any]]:
        """Informationen zu Kunstwerken Tests (10 tests)"""
        return [
            {
                "id": 111,
                "category": "artwork_info",
                "description": "Mona Lisa information",
                "input": "Erzähl mir etwas über die Mona Lisa.",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Mona Lisa"]
            },
            {
                "id": 112,
                "category": "artwork_info",
                "description": "Last Supper information",
                "input": "Was weißt du über Das letzte Abendmahl?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Das letzte Abendmahl"]
            },
            {
                "id": 113,
                "category": "artwork_info",
                "description": "Starry Night artist question",
                "input": "Wer hat Die Sternennacht gemalt?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Die Sternennacht"]
            },
            {
                "id": 114,
                "category": "artwork_info",
                "description": "Guernica details",
                "input": "Welche Details gibt es zum Gemälde Guernica?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Guernica"]
            },
            {
                "id": 115,
                "category": "artwork_info",
                "description": "The Scream background",
                "input": "Gibt es Hintergrundinfos zu Der Schrei von Edvard Munch?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Der Schrei"]
            },
            {
                "id": 116,
                "category": "artwork_info",
                "description": "Creation of Adam location",
                "input": "Wo steht Die Erschaffung Adams aus der Sixtinischen Kapelle?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Die Erschaffung Adams"]
            },
            {
                "id": 117,
                "category": "artwork_info",
                "description": "Night Watch title meaning",
                "input": "Was bedeutet der Titel Die Nachtwache von Rembrandt?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Die Nachtwache"]
            },
            {
                "id": 118,
                "category": "artwork_info",
                "description": "Birth of Venus style",
                "input": "Erkläre mir kurz den Stil von Die Geburt der Venus.",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Die Geburt der Venus"]
            },
            {
                "id": 119,
                "category": "artwork_info",
                "description": "Guernica museum location",
                "input": "In welchem Museum kann ich Guernica sehen?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Guernica"]
            },
            {
                "id": 120,
                "category": "artwork_info",
                "description": "Wanderer above the Sea of Fog facts",
                "input": "Gibt es interessante Fakten zu Der Wanderer über dem Nebelmeer?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Der Wanderer über dem Nebelmeer"]
            }
        ]
    
    @staticmethod
    def artist_info_tests() -> List[Dict[str, Any]]:
        """Künstler-Informationen Tests (10 tests)"""
        return [
            {
                "id": 121,
                "category": "artist_info",
                "description": "Vincent van Gogh biography",
                "input": "Wer war Vincent van Gogh?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Vincent van Gogh"]
            },
            {
                "id": 122,
                "category": "artist_info",
                "description": "Pablo Picasso information",
                "input": "Erzähl mir etwas über Pablo Picasso.",
                "expected_intent": "ask_artist",
                "expected_entities": ["Pablo Picasso"]
            },
            {
                "id": 123,
                "category": "artist_info",
                "description": "Leonardo da Vinci birthplace",
                "input": "Wo wurde Leonardo da Vinci geboren?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Leonardo da Vinci"]
            },
            {
                "id": 124,
                "category": "artist_info",
                "description": "Frida Kahlo life and work",
                "input": "Wann lebte Frida Kahlo und was ist ihr bekanntestes Werk?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Frida Kahlo"]
            },
            {
                "id": 125,
                "category": "artist_info",
                "description": "Henri Matisse art movement",
                "input": "Welche Kunstrichtung vertrat Henri Matisse?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Henri Matisse"]
            },
            {
                "id": 126,
                "category": "artist_info",
                "description": "Michelangelo Buonarroti details",
                "input": "Gibt es spannende Details zu Michelangelo Buonarroti?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Michelangelo Buonarroti"]
            },
            {
                "id": 127,
                "category": "artist_info",
                "description": "Gustav Klimt characteristics",
                "input": "Was zeichnet Gustav Klimt aus?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Gustav Klimt"]
            },
            {
                "id": 128,
                "category": "artist_info",
                "description": "Georgia O'Keeffe biography",
                "input": "Kannst du mir eine kurze Biografie von Georgia O'Keeffe geben?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Georgia O'Keeffe"]
            },
            {
                "id": 129,
                "category": "artist_info",
                "description": "Salvador Dalí famous painting",
                "input": "Was war Salvador Dalís berühmtestes Gemälde?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Salvador Dalí"]
            },
            {
                "id": 130,
                "category": "artist_info",
                "description": "Auguste Rodin awards",
                "input": "Welche Auszeichnungen bekam Auguste Rodin?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Auguste Rodin"]
            }
        ]
    
    @staticmethod
    def museum_info_tests() -> List[Dict[str, Any]]:
        """Museumsinformationen Tests (8 tests)"""
        return [
            {
                "id": 131,
                "category": "museum_info",
                "description": "Mona Lisa museum location",
                "input": "In welchem Museum hängt die Mona Lisa?",
                "expected_intent": "ask_museum_info",
                "expected_entities": ["Mona Lisa", "Museum"]
            },
            {
                "id": 132,
                "category": "museum_info",
                "description": "Louvre opening hours",
                "input": "Öffnungszeiten des Louvre in Paris?",
                "expected_intent": "ask_opening_hours",
                "expected_entities": ["Louvre"]
            },
            {
                "id": 133,
                "category": "museum_info",
                "description": "Rijksmuseum ticket prices",
                "input": "Wie sind die Eintrittspreise für das Rijksmuseum?",
                "expected_intent": "ask_ticket_price",
                "expected_entities": ["Rijksmuseum"]
            },
            {
                "id": 134,
                "category": "museum_info",
                "description": "Prado special exhibitions",
                "input": "Gibt es gerade Sonderausstellungen im Prado?",
                "expected_intent": "ask_exhibitions",
                "expected_entities": ["Prado"]
            },
            {
                "id": 135,
                "category": "museum_info",
                "description": "Van Gogh Museum location",
                "input": "Wo befindet sich das Van-Gogh-Museum?",
                "expected_intent": "ask_location",
                "expected_entities": ["Van-Gogh-Museum"]
            },
            {
                "id": 136,
                "category": "museum_info",
                "description": "Guggenheim Sunday opening",
                "input": "Ist das Guggenheim-Museum in New York auch sonntags geöffnet?",
                "expected_intent": "ask_opening_hours",
                "expected_entities": ["Guggenheim-Museum", "sonntags"]
            },
            {
                "id": 137,
                "category": "museum_info",
                "description": "Uffizi Gallery departments",
                "input": "Welche Abteilungen hat die Uffizien-Galerie in Florenz?",
                "expected_intent": "ask_museum_info",
                "expected_entities": ["Uffizien-Galerie"]
            },
            {
                "id": 138,
                "category": "museum_info",
                "description": "Paris museum card",
                "input": "Gibt es eine Museumskarte für Paris?",
                "expected_intent": "ask_museum_card",
                "expected_entities": ["Paris", "Museumskarte"]
            }
        ]
    
    @staticmethod
    def gratitude_tests() -> List[Dict[str, Any]]:
        """Dankbarkeit Tests (3 tests)"""
        return [
            {
                "id": 139,
                "category": "gratitude",
                "description": "Thank you for help",
                "input": "Danke für deine Hilfe!",
                "expected_intent": "thanks"
            },
            {
                "id": 140,
                "category": "gratitude",
                "description": "Simple thank you",
                "input": "Vielen Dank!",
                "expected_intent": "thanks"
            },
            {
                "id": 141,
                "category": "gratitude",
                "description": "Appreciative thanks",
                "input": "Super, das hat mir sehr geholfen!",
                "expected_intent": "thanks"
            }
        ]
    
    @staticmethod
    def help_support_tests() -> List[Dict[str, Any]]:
        """Hilfe/Support Tests (4 tests)"""
        return [
            {
                "id": 142,
                "category": "help_support",
                "description": "How to use best",
                "input": "Wie nutze ich dich am besten?",
                "expected_intent": "ask_help"
            },
            {
                "id": 143,
                "category": "help_support",
                "description": "What can you answer",
                "input": "Was kannst du alles beantworten?",
                "expected_intent": "ask_capabilities"
            },
            {
                "id": 144,
                "category": "help_support",
                "description": "Confused user",
                "input": "Ich weiß nicht, was ich hier machen soll.",
                "expected_intent": "ask_help"
            },
            {
                "id": 145,
                "category": "help_support",
                "description": "How to ask about painting",
                "input": "Wie formuliere ich eine Frage zu einem Gemälde?",
                "expected_intent": "ask_help"
            }
        ]
    
    @staticmethod
    def small_talk_tests() -> List[Dict[str, Any]]:
        """Small Talk Tests (5 tests)"""
        return [
            {
                "id": 146,
                "category": "small_talk",
                "description": "Favorite topic",
                "input": "Was ist dein Lieblingsthema?",
                "expected_intent": "small_talk"
            },
            {
                "id": 147,
                "category": "small_talk",
                "description": "Tell me a joke",
                "input": "Erzähl mir einen Witz.",
                "expected_intent": "small_talk"
            },
            {
                "id": 148,
                "category": "small_talk",
                "description": "Opinion on modern art",
                "input": "Wie findest du moderne Kunst?",
                "expected_intent": "small_talk"
            },
            {
                "id": 149,
                "category": "small_talk",
                "description": "Favorite color",
                "input": "Hast du eine Lieblingsfarbe?",
                "expected_intent": "small_talk"
            },
            {
                "id": 150,
                "category": "small_talk",
                "description": "AI in art opinion",
                "input": "Was hältst du von AI im Kunstbereich?",
                "expected_intent": "small_talk"
            }
        ]
    
    def get_all_test_cases(self) -> List[Dict[str, Any]]:
        """Returns all new test cases combined"""
        all_tests = []
        all_tests.extend(self.greeting_tests())
        all_tests.extend(self.farewell_tests())
        all_tests.extend(self.artwork_info_tests())
        all_tests.extend(self.artist_info_tests())
        all_tests.extend(self.museum_info_tests())
        all_tests.extend(self.gratitude_tests())
        all_tests.extend(self.help_support_tests())
        all_tests.extend(self.small_talk_tests())
        return all_tests
    
    def get_tests_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Returns test cases for a specific category"""
        category_methods = {
            "greeting": self.greeting_tests,
            "farewell": self.farewell_tests,
            "artwork_info": self.artwork_info_tests,
            "artist_info": self.artist_info_tests,
            "museum_info": self.museum_info_tests,
            "gratitude": self.gratitude_tests,
            "help_support": self.help_support_tests,
            "small_talk": self.small_talk_tests
        }
        
        if category in category_methods:
            return category_methods[category]()
        else:
            return []
    
    def get_test_statistics(self) -> Dict[str, int]:
        """Returns statistics about test cases by category"""
        stats = {
            "greeting": len(self.greeting_tests()),
            "farewell": len(self.farewell_tests()),
            "artwork_info": len(self.artwork_info_tests()),
            "artist_info": len(self.artist_info_tests()),
            "museum_info": len(self.museum_info_tests()),
            "gratitude": len(self.gratitude_tests()),
            "help_support": len(self.help_support_tests()),
            "small_talk": len(self.small_talk_tests())
        }
        stats["total"] = sum(stats.values())
        return stats
