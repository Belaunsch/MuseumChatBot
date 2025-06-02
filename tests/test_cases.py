#!/usr/bin/env python3
"""
Test case definitions for the Museum Guide Chatbot
Organized collection of test cases by category
"""

from typing import List, Dict, Any


class TestCaseProvider:
    """Collection of all test cases organized by categories"""
    
    @staticmethod
    def artwork_tests() -> List[Dict[str, Any]]:
        """Artwork tests (10 tests)"""
        return [
            {
                "id": 1,
                "category": "artwork",
                "description": "Famous painting - Mona Lisa",
                "input": "Erzähl mir etwas über die Mona Lisa",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Mona Lisa"]
            },
            {
                "id": 2,
                "category": "artwork", 
                "description": "Van Gogh painting - Starry Night",
                "input": "Was weißt du über The Starry Night?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["The Starry Night"]
            },
            {
                "id": 3,
                "category": "artwork",
                "description": "Picasso work - Guernica",
                "input": "Informationen zu Guernica bitte",
                "expected_intent": "ask_artwork", 
                "expected_entities": ["Guernica"]
            },
            {
                "id": 4,
                "category": "artwork",
                "description": "Vermeer painting - Girl with a Pearl Earring",
                "input": "Erzähl mir von Girl with a Pearl Earring",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Girl with a Pearl Earring"]
            },
            {
                "id": 5,
                "category": "artwork",
                "description": "Munch painting - The Scream",
                "input": "Was ist Der Schrei?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Der Schrei"]
            },
            {
                "id": 6,
                "category": "artwork",
                "description": "Hokusai work - The Great Wave",
                "input": "Details zu The Great Wave off Kanagawa",
                "expected_intent": "ask_artwork",
                "expected_entities": ["The Great Wave off Kanagawa"]
            },
            {
                "id": 7,
                "category": "artwork",
                "description": "American Gothic",
                "input": "Wer hat American Gothic gemalt?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["American Gothic"]
            },
            {
                "id": 8,
                "category": "artwork",
                "description": "Dalí work - Persistence of Memory",
                "input": "The Persistence of Memory Informationen",
                "expected_intent": "ask_artwork",
                "expected_entities": ["The Persistence of Memory"]
            },
            {
                "id": 9,
                "category": "artwork",
                "description": "Velázquez - Las Meninas",
                "input": "Erzähl mir etwas über Las Meninas",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Las Meninas"]
            },            {
                "id": 10,
                "category": "artwork",
                "description": "Van Gogh - Wheat Field with Cypresses",
                "input": "Was weißt du über Wheat Field with Cypresses?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Wheat Field with Cypresses"]
            },
            # Neue Artwork-Tests (11-20)
            {
                "id": 31,
                "category": "artwork",
                "description": "Rodin sculpture - The Thinker",
                "input": "Erzähl mir etwas über Der Denker von Rodin",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Der Denker"]
            },
            {
                "id": 32,
                "category": "artwork", 
                "description": "Botticelli - The Birth of Venus",
                "input": "Was ist Die Geburt der Venus?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Die Geburt der Venus"]
            },
            {
                "id": 33,
                "category": "artwork",
                "description": "Michelangelo - David",
                "input": "Informationen über den David von Michelangelo",
                "expected_intent": "ask_artwork",
                "expected_entities": ["David"]
            },
            {
                "id": 34,
                "category": "artwork",
                "description": "Manet - Olympia",
                "input": "Wer hat Olympia gemalt?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Olympia"]
            },
            {
                "id": 35,
                "category": "artwork",
                "description": "Cézanne - The Card Players",
                "input": "Details zu Die Kartenspieler",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Die Kartenspieler"]
            },
            {
                "id": 36,
                "category": "artwork",
                "description": "Kandinsky - Composition VII",
                "input": "Erzähl mir von Komposition VII",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Komposition VII"]
            },
            {
                "id": 37,
                "category": "artwork",
                "description": "Matisse - Woman with a Hat",
                "input": "Was weißt du über Woman with a Hat?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Woman with a Hat"]
            },
            {
                "id": 38,
                "category": "artwork",
                "description": "Turner - The Fighting Temeraire",
                "input": "Informationen zu The Fighting Temeraire",
                "expected_intent": "ask_artwork",
                "expected_entities": ["The Fighting Temeraire"]
            },
            {
                "id": 39,
                "category": "artwork",
                "description": "Seurat - A Sunday on La Grande Jatte",
                "input": "Erzähl mir über Ein Sonntag auf La Grande Jatte",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Ein Sonntag auf La Grande Jatte"]
            },
            {
                "id": 40,
                "category": "artwork",
                "description": "Pollock - Number 1",
                "input": "Was ist Number 1 von Jackson Pollock?",
                "expected_intent": "ask_artwork",
                "expected_entities": ["Number 1"]
            }
        ]
    
    @staticmethod
    def artist_tests() -> List[Dict[str, Any]]:
        """Artist tests (8 tests)"""
        return [
            {
                "id": 11,
                "category": "artist",
                "description": "Vincent van Gogh biography",
                "input": "Wer war Vincent van Gogh?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Vincent van Gogh"]
            },
            {
                "id": 12,
                "category": "artist",
                "description": "Pablo Picasso information",
                "input": "Erzähl mir etwas über Pablo Picasso",
                "expected_intent": "ask_artist",
                "expected_entities": ["Pablo Picasso"]
            },
            {
                "id": 13,
                "category": "artist",
                "description": "Leonardo da Vinci",
                "input": "Was weißt du über Leonardo da Vinci?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Leonardo da Vinci"]
            },
            {
                "id": 14,
                "category": "artist",
                "description": "Frida Kahlo",
                "input": "Wann wurde Frida Kahlo geboren?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Frida Kahlo"]
            },
            {
                "id": 15,
                "category": "artist",
                "description": "Claude Monet",
                "input": "Informationen zu Claude Monet bitte",
                "expected_intent": "ask_artist",
                "expected_entities": ["Claude Monet"]
            },
            {
                "id": 16,
                "category": "artist",
                "description": "Rembrandt (with typo)",
                "input": "Wer war Rembrandzt?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Rembrandzt"]
            },
            {
                "id": 17,
                "category": "artist",
                "description": "Andy Warhol",
                "input": "Erzähl mir von Andy Warhol",
                "expected_intent": "ask_artist",
                "expected_entities": ["Andy Warhol"]
            },            {
                "id": 18,
                "category": "artist",
                "description": "Georgia O'Keeffe",
                "input": "Wann ist Georgia O'Keeffe gestorben?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Georgia O'Keeffe"]
            },
            # Neue Artist-Tests (19-25)
            {
                "id": 41,
                "category": "artist",
                "description": "Salvador Dalí",
                "input": "Erzähl mir etwas über Salvador Dalí",
                "expected_intent": "ask_artist",
                "expected_entities": ["Salvador Dalí"]
            },
            {
                "id": 42,
                "category": "artist",
                "description": "Henri Matisse",
                "input": "Wer war Henri Matisse?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Henri Matisse"]
            },
            {
                "id": 43,
                "category": "artist",
                "description": "Jackson Pollock",
                "input": "Informationen zu Jackson Pollock bitte",
                "expected_intent": "ask_artist",
                "expected_entities": ["Jackson Pollock"]
            },
            {
                "id": 44,
                "category": "artist",
                "description": "Wassily Kandinsky",
                "input": "Was weißt du über Wassily Kandinsky?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Wassily Kandinsky"]
            },
            {
                "id": 45,
                "category": "artist",
                "description": "Auguste Rodin",
                "input": "Wann lebte Auguste Rodin?",
                "expected_intent": "ask_artist",
                "expected_entities": ["Auguste Rodin"]
            },
            {
                "id": 46,
                "category": "artist",
                "description": "Paul Cézanne",
                "input": "Erzähl mir von Paul Cézanne",
                "expected_intent": "ask_artist",
                "expected_entities": ["Paul Cézanne"]
            },
            {
                "id": 47,
                "category": "artist",
                "description": "Édouard Manet",
                "input": "Biografie von Édouard Manet",
                "expected_intent": "ask_artist",
                "expected_entities": ["Édouard Manet"]
            }
        ]
    
    @staticmethod
    def museum_tests() -> List[Dict[str, Any]]:
        """Museum tests (7 tests)"""
        return [
            {
                "id": 19,
                "category": "museum",
                "description": "Louvre opening hours",
                "input": "Wann öffnet das Louvre heute?",
                "expected_intent": "ask_opening_hours",
                "expected_entities": ["Louvre", "heute"]
            },
            {
                "id": 20,
                "category": "museum",
                "description": "MoMA location",
                "input": "Wo befindet sich das MoMA?",
                "expected_intent": "ask_location",
                "expected_entities": ["MoMA"]
            },
            {
                "id": 21,
                "category": "museum",
                "description": "Van Gogh Museum prices",
                "input": "Wie teuer ist der Eintritt ins Van Gogh Museum?",
                "expected_intent": "ask_ticket_price",
                "expected_entities": ["Van Gogh Museum"]
            },
            {
                "id": 22,
                "category": "museum",
                "description": "British Museum address",
                "input": "Adresse des British Museum?",
                "expected_intent": "ask_location",
                "expected_entities": ["British Museum"]
            },
            {
                "id": 23,
                "category": "museum",
                "description": "Guggenheim opening hours",
                "input": "Ist das Guggenheim Museum gerade geöffnet?",
                "expected_intent": "ask_opening_hours",
                "expected_entities": ["Guggenheim Museum", "gerade"]
            },
            {
                "id": 24,
                "category": "museum",
                "description": "Rijksmuseum information",
                "input": "Erzähl mir etwas über das Rijksmuseum",
                "expected_intent": "ask_museum_info",
                "expected_entities": ["Rijksmuseum"]
            },            {
                "id": 25,
                "category": "museum",
                "description": "Tate Modern",
                "input": "Öffnungszeiten Tate Modern?",
                "expected_intent": "ask_opening_hours",
                "expected_entities": ["Tate Modern"]
            },
            # Neue Museum-Tests (26-32)
            {
                "id": 48,
                "category": "museum",
                "description": "Metropolitan Museum ticket prices",
                "input": "Was kostet der Eintritt ins Metropolitan Museum?",
                "expected_intent": "ask_ticket_price",
                "expected_entities": ["Metropolitan Museum"]
            },
            {
                "id": 49,
                "category": "museum",
                "description": "Uffizi Gallery location",
                "input": "Wo ist die Uffizi Galerie?",
                "expected_intent": "ask_location",
                "expected_entities": ["Uffizi Galerie"]
            },
            {
                "id": 50,
                "category": "museum",
                "description": "Prado Museum opening hours",
                "input": "Wann hat das Prado Museum geöffnet?",
                "expected_intent": "ask_opening_hours",
                "expected_entities": ["Prado Museum"]
            },
            {
                "id": 51,
                "category": "museum",
                "description": "Hermitage information",
                "input": "Erzähl mir etwas über die Eremitage",
                "expected_intent": "ask_museum_info",
                "expected_entities": ["Eremitage"]
            },
            {
                "id": 52,
                "category": "museum",
                "description": "National Gallery address",
                "input": "Adresse der National Gallery London?",
                "expected_intent": "ask_location",
                "expected_entities": ["National Gallery"]
            },
            {
                "id": 53,
                "category": "museum",
                "description": "Musée d'Orsay prices",
                "input": "Wie teuer ist das Musée d'Orsay?",
                "expected_intent": "ask_ticket_price",
                "expected_entities": ["Musée d'Orsay"]
            },
            {
                "id": 54,
                "category": "museum",
                "description": "Centre Pompidou opening status",
                "input": "Ist das Centre Pompidou heute offen?",
                "expected_intent": "ask_opening_hours",
                "expected_entities": ["Centre Pompidou", "heute"]
            }
        ]
    
    @staticmethod
    def conversation_tests() -> List[Dict[str, Any]]:
        """Conversation tests (5 tests)"""
        return [
            {
                "id": 26,
                "category": "conversation",
                "description": "Greeting",
                "input": "Hallo",
                "expected_intent": "greet"
            },
            {
                "id": 27,
                "category": "conversation",
                "description": "Bot challenge",
                "input": "Bist du ein Bot?",
                "expected_intent": "bot_challenge"
            },
            {
                "id": 28,
                "category": "conversation",
                "description": "Thanks",
                "input": "Vielen Dank",
                "expected_intent": "thanks"
            },
            {
                "id": 29,
                "category": "conversation",
                "description": "Goodbye",
                "input": "Tschüss",
                "expected_intent": "goodbye"
            },            {
                "id": 30,
                "category": "conversation",
                "description": "Incomprehensible input",
                "input": "xyz123 blablabla nonsense",
                "expected_intent": "nlu_fallback"
            },
            # Neue Conversation-Tests (31-37)
            {
                "id": 55,
                "category": "conversation",
                "description": "Help request",
                "input": "Kannst du mir helfen?",
                "expected_intent": "ask_help"
            },
            {
                "id": 56,
                "category": "conversation",
                "description": "What can you do",
                "input": "Was kannst du alles?",
                "expected_intent": "ask_capabilities"
            },
            {
                "id": 57,
                "category": "conversation",
                "description": "Good morning",
                "input": "Guten Morgen!",
                "expected_intent": "greet"
            },
            {
                "id": 58,
                "category": "conversation",
                "description": "Repeat request",
                "input": "Kannst du das nochmal sagen?",
                "expected_intent": "ask_repeat"
            },
            {
                "id": 59,
                "category": "conversation",
                "description": "How are you",
                "input": "Wie geht es dir?",
                "expected_intent": "ask_how_are_you"
            },
            {
                "id": 60,
                "category": "conversation",
                "description": "See you later",
                "input": "Bis später!",
                "expected_intent": "goodbye"
            },
            {
                "id": 61,
                "category": "conversation",
                "description": "Another nonsense input",
                "input": "qwerty asdfgh zxcvbn 12345",
                "expected_intent": "nlu_fallback"
            }
        ]
    
    @staticmethod
    def art_movement_tests() -> List[Dict[str, Any]]:
        """Art movement tests - Neue Kategorie (7 tests)"""
        return [
            {
                "id": 62,
                "category": "art_movement",
                "description": "Impressionism",
                "input": "Was ist Impressionismus?",
                "expected_intent": "ask_art_movement",
                "expected_entities": ["Impressionismus"]
            },
            {
                "id": 63,
                "category": "art_movement",
                "description": "Cubism",
                "input": "Erzähl mir etwas über den Kubismus",
                "expected_intent": "ask_art_movement",
                "expected_entities": ["Kubismus"]
            },
            {
                "id": 64,
                "category": "art_movement",
                "description": "Surrealism",
                "input": "Was charakterisiert den Surrealismus?",
                "expected_intent": "ask_art_movement",
                "expected_entities": ["Surrealismus"]
            },
            {
                "id": 65,
                "category": "art_movement",
                "description": "Abstract Expressionism",
                "input": "Informationen zum Abstrakten Expressionismus",
                "expected_intent": "ask_art_movement",
                "expected_entities": ["Abstrakten Expressionismus"]
            },
            {
                "id": 66,
                "category": "art_movement",
                "description": "Renaissance",
                "input": "Erzähl mir von der Renaissance",
                "expected_intent": "ask_art_movement",
                "expected_entities": ["Renaissance"]
            },
            {
                "id": 67,
                "category": "art_movement",
                "description": "Baroque",
                "input": "Was ist der Barock?",
                "expected_intent": "ask_art_movement",
                "expected_entities": ["Barock"]
            },
            {
                "id": 68,
                "category": "art_movement",
                "description": "Pop Art",
                "input": "Details zur Pop Art bitte",
                "expected_intent": "ask_art_movement",
                "expected_entities": ["Pop Art"]
            }
        ]
    
    @staticmethod
    def practical_tests() -> List[Dict[str, Any]]:
        """Practical visitor information tests - Neue Kategorie (6 tests)"""
        return [
            {
                "id": 69,
                "category": "practical",
                "description": "Parking information",
                "input": "Gibt es Parkplätze am Museum?",
                "expected_intent": "ask_parking",
                "expected_entities": []
            },
            {
                "id": 70,
                "category": "practical",
                "description": "Accessibility information",
                "input": "Ist das Museum barrierefrei?",
                "expected_intent": "ask_accessibility",
                "expected_entities": []
            },
            {
                "id": 71,
                "category": "practical",
                "description": "Guided tours",
                "input": "Gibt es Führungen?",
                "expected_intent": "ask_guided_tours",
                "expected_entities": []
            },
            {
                "id": 72,
                "category": "practical",
                "description": "Photography rules",
                "input": "Darf ich hier fotografieren?",
                "expected_intent": "ask_photography",
                "expected_entities": []
            },
            {
                "id": 73,
                "category": "practical",
                "description": "Restaurant/Cafe",
                "input": "Hat das Museum ein Café?",
                "expected_intent": "ask_cafe",
                "expected_entities": []
            },
            {
                "id": 74,
                "category": "practical",
                "description": "Gift shop",
                "input": "Wo ist der Museumsshop?",
                "expected_intent": "ask_gift_shop",
                "expected_entities": []
            }
        ]
    def get_all_test_cases(self) -> List[Dict[str, Any]]:
        """Returns all test cases combined"""
        all_tests = []
        all_tests.extend(self.artwork_tests())
        all_tests.extend(self.artist_tests()) 
        all_tests.extend(self.museum_tests())
        all_tests.extend(self.conversation_tests())
        all_tests.extend(self.art_movement_tests())
        all_tests.extend(self.practical_tests())
        return all_tests
    
    def get_tests_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Returns test cases for a specific category"""
        category_methods = {
            "artwork": self.artwork_tests,
            "artist": self.artist_tests,
            "museum": self.museum_tests,
            "conversation": self.conversation_tests,
            "art_movement": self.art_movement_tests,
            "practical": self.practical_tests
        }
        
        if category in category_methods:
            return category_methods[category]()
        else:
            return []
