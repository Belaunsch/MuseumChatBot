#!/usr/bin/env python3
"""
Hilfsskript für die neuen Museum Chatbot Tests
Bietet verschiedene Funktionen zum Ausführen und Verwalten der Tests
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

# Add project directory to path
sys.path.append(os.path.dirname(__file__))

from new_test_cases import NewTestCaseProvider


class NewTestUtilities:
    """Hilfsklasse für neue Testfälle"""
    
    def __init__(self):
        self.provider = NewTestCaseProvider()
    
    def export_test_cases_to_json(self, filename: str = None) -> str:
        """Exportiert alle Testfälle als JSON-Datei"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"new_test_cases_export_{timestamp}.json"
        
        test_cases = self.provider.get_all_test_cases()
        stats = self.provider.get_test_statistics()
        
        export_data = {
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "total_tests": stats['total'],
                "categories": {k: v for k, v in stats.items() if k != 'total'}
            },
            "test_cases": test_cases
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Testfälle exportiert nach: {filename}")
        return filename
    
    def generate_test_report(self) -> None:
        """Generiert einen detaillierten Testbericht"""
        stats = self.provider.get_test_statistics()
        test_cases = self.provider.get_all_test_cases()
        
        print("📋 DETAILLIERTER TESTBERICHT")
        print("=" * 60)
        print(f"Generiert am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Gesamt Testfälle: {stats['total']}")
        print()
        
        # Kategorieübersicht
        print("📊 KATEGORIEÜBERSICHT:")
        print("-" * 40)
        for category, count in stats.items():
            if category != 'total':
                percentage = (count / stats['total'] * 100)
                print(f"{category:20} | {count:3d} Tests ({percentage:5.1f}%)")
        
        print()
        print("📝 TESTFÄLLE NACH KATEGORIEN:")
        print("-" * 60)
        
        # Details für jede Kategorie
        for category in stats.keys():
            if category != 'total':
                category_tests = self.provider.get_tests_by_category(category)
                print(f"\n🔸 {category.upper()} ({len(category_tests)} Tests):")
                
                for i, test in enumerate(category_tests, 1):
                    print(f"   {i:2d}. ID {test['id']:3d}: {test['description']}")
                    print(f"       Input: \"{test['input']}\"")
                    if 'expected_intent' in test:
                        print(f"       Expected Intent: {test['expected_intent']}")
                    if 'expected_entities' in test:
                        print(f"       Expected Entities: {test['expected_entities']}")
                    print()
        
        print("=" * 60)
    
    def validate_test_cases(self) -> bool:
        """Validiert die Testfälle auf Konsistenz"""
        print("🔍 VALIDIERE TESTFÄLLE...")
        print("-" * 40)
        
        test_cases = self.provider.get_all_test_cases()
        errors = []
        warnings = []
        
        # Track IDs to check for duplicates
        seen_ids = set()
        
        for test in test_cases:
            test_id = test.get('id')
            
            # Check for required fields
            required_fields = ['id', 'category', 'description', 'input']
            for field in required_fields:
                if field not in test:
                    errors.append(f"Test ID {test_id}: Fehlendes Feld '{field}'")
            
            # Check for duplicate IDs
            if test_id in seen_ids:
                errors.append(f"Test ID {test_id}: Doppelte ID")
            seen_ids.add(test_id)
            
            # Check input length
            input_text = test.get('input', '')
            if len(input_text) < 3:
                warnings.append(f"Test ID {test_id}: Sehr kurzer Input '{input_text}'")
            
            # Check for expected_intent
            if 'expected_intent' not in test:
                warnings.append(f"Test ID {test_id}: Kein expected_intent definiert")
        
        # Print results
        if errors:
            print("❌ FEHLER GEFUNDEN:")
            for error in errors:
                print(f"   • {error}")
        
        if warnings:
            print("⚠️ WARNUNGEN:")
            for warning in warnings:
                print(f"   • {warning}")
        
        if not errors and not warnings:
            print("✅ Alle Testfälle sind valide!")
        
        print(f"\nValidierung abgeschlossen: {len(errors)} Fehler, {len(warnings)} Warnungen")
        return len(errors) == 0
    
    def find_tests_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Findet Testfälle basierend auf einem Schlüsselwort"""
        test_cases = self.provider.get_all_test_cases()
        matching_tests = []
        
        keyword_lower = keyword.lower()
        
        for test in test_cases:
            # Search in input, description, and category
            if (keyword_lower in test.get('input', '').lower() or
                keyword_lower in test.get('description', '').lower() or
                keyword_lower in test.get('category', '').lower()):
                matching_tests.append(test)
        
        return matching_tests
    
    def print_tests_by_keyword(self, keyword: str) -> None:
        """Druckt Testfälle die ein Schlüsselwort enthalten"""
        matching_tests = self.find_tests_by_keyword(keyword)
        
        print(f"🔍 TESTFÄLLE MIT SCHLÜSSELWORT '{keyword}':")
        print("-" * 50)
        
        if not matching_tests:
            print("Keine passenden Testfälle gefunden.")
            return
        
        for test in matching_tests:
            print(f"ID {test['id']:3d} | {test['category']:15} | {test['description']}")
            print(f"        Input: \"{test['input']}\"")
            print()
        
        print(f"Gefunden: {len(matching_tests)} Testfälle")


def main():
    """Hauptfunktion für das Hilfsskript"""
    utils = NewTestUtilities()
    
    if len(sys.argv) == 1:
        print("🛠️ Museum Chatbot Test Utilities")
        print("=" * 40)
        print("Verfügbare Kommandos:")
        print("  report     - Detaillierten Testbericht generieren")
        print("  validate   - Testfälle validieren")
        print("  export     - Testfälle als JSON exportieren")
        print("  search [keyword] - Nach Testfällen suchen")
        print("  stats      - Kurze Statistik anzeigen")
        return
    
    command = sys.argv[1].lower()
    
    if command == "report":
        utils.generate_test_report()
    
    elif command == "validate":
        utils.validate_test_cases()
    
    elif command == "export":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        utils.export_test_cases_to_json(filename)
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Bitte geben Sie ein Schlüsselwort an")
            return
        keyword = sys.argv[2]
        utils.print_tests_by_keyword(keyword)
    
    elif command == "stats":
        stats = utils.provider.get_test_statistics()
        print("📊 TEST STATISTIK:")
        print("-" * 30)
        for category, count in stats.items():
            if category != 'total':
                print(f"{category:20} | {count:3d}")
        print("-" * 30)
        print(f"{'GESAMT':20} | {stats['total']:3d}")
    
    else:
        print(f"❌ Unbekanntes Kommando: {command}")
        print("Verwenden Sie das Skript ohne Argumente für Hilfe")


if __name__ == "__main__":
    main()
