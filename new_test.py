#!/usr/bin/env python3
"""
Neuer Testläufer für den Museum Guide Chatbot
Führt die neuen erweiterten Testfälle aus
"""

import sys
import os
import time
from datetime import datetime

# Add tests directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

from new_test_cases import NewTestCaseProvider
from tests.utils.test_runner import TestRunner
from tests.utils.results_saver import ResultsSaver
from tests.config import SERVER_CONFIG


class NewChatbotTester:
    """Neuer Haupttest-Orchestrator für erweiterte Testfälle"""
    
    def __init__(self):
        self.test_case_provider = NewTestCaseProvider()
        self.test_runner = TestRunner()
        self.results_saver = ResultsSaver()
    
    def run_all_tests(self):
        """Führt die komplette neue Testsuite aus"""
        print("🤖 Museum Guide Chatbot - Neue Erweiterte Tests")
        print("=" * 70)
        
        # Get test cases
        test_cases = self.test_case_provider.get_all_test_cases()
        stats = self.test_case_provider.get_test_statistics()
        
        # Print statistics
        print(f"📊 Gesamt Testfälle: {stats['total']}")
        print("📋 Kategorien:")
        for category, count in stats.items():
            if category != 'total':
                print(f"   • {category}: {count} Tests")
        print("-" * 70)
        
        # Check server health
        print("🔍 Überprüfe Rasa Server...")
        if not self.test_runner.check_server_health():
            print("❌ Server nicht verfügbar. Teste beenden.")
            return False
        
        print("✅ Server ist bereit!")
        print("-" * 70)
        
        # Run tests
        print("🚀 Starte Testausführung...")
        test_results = self.test_runner.run_all_tests(test_cases)
        
        if test_results:
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"new_test_results_{timestamp}.json"
            saved_file = self.results_saver.save_results(
                test_results, 
                results_file
            )
            
            # Print summary
            self._print_test_summary(test_results, stats)
            
            if saved_file:
                print(f"💾 Ergebnisse gespeichert in: {saved_file}")
            
            return True
        else:
            print("❌ Keine Testergebnisse erhalten")
            return False
    
    def run_category_tests(self, category: str):
        """Führt Tests für eine spezifische Kategorie aus"""
        print(f"🤖 Museum Guide Chatbot - Tests für Kategorie: {category}")
        print("=" * 70)
        
        # Get test cases for category
        test_cases = self.test_case_provider.get_tests_by_category(category)
        
        if not test_cases:
            print(f"❌ Keine Tests für Kategorie '{category}' gefunden")
            return False
        
        print(f"📊 Tests für Kategorie '{category}': {len(test_cases)}")
        print("-" * 70)
        
        # Check server health
        print("🔍 Überprüfe Rasa Server...")
        if not self.test_runner.check_server_health():
            print("❌ Server nicht verfügbar. Teste beenden.")
            return False
        
        print("✅ Server ist bereit!")
        print("-" * 70)
        
        # Run tests
        print("🚀 Starte Testausführung...")
        test_results = self.test_runner.run_all_tests(test_cases)
        
        if test_results:
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = f"new_test_results_{category}_{timestamp}.json"
            saved_file = self.results_saver.save_results(
                test_results, 
                results_file
            )
            
            # Print summary
            category_stats = {category: len(test_cases), 'total': len(test_cases)}
            self._print_test_summary(test_results, category_stats)
            
            if saved_file:
                print(f"💾 Ergebnisse gespeichert in: {saved_file}")
            
            return True
        else:
            print("❌ Keine Testergebnisse erhalten")
            return False
    
    def _print_test_summary(self, test_results: list, stats: dict):
        """Druckt eine Zusammenfassung der Testergebnisse"""
        print("\n" + "=" * 70)
        print("📈 TESTZUSAMMENFASSUNG")
        print("=" * 70)
        
        # Calculate results by status
        status_counts = {}
        category_results = {}
        total_response_time = 0
        
        for result in test_results:
            # Status counts
            status = result.get('evaluation', 'UNKNOWN')
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Category results
            category = result.get('category', 'unknown')
            if category not in category_results:
                category_results[category] = {'total': 0, 'passed': 0}
            category_results[category]['total'] += 1
            if status == 'PASS':
                category_results[category]['passed'] += 1
            
            # Response time
            total_response_time += result.get('response_time', 0)
        
        # Print overall results
        total_tests = len(test_results)
        passed_tests = status_counts.get('PASS', 0)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        avg_response_time = (total_response_time / total_tests) if total_tests > 0 else 0
        
        print(f"Gesamt Tests: {total_tests}")
        print(f"Erfolgreich: {passed_tests} ({success_rate:.1f}%)")
        print(f"Durchschnittliche Antwortzeit: {avg_response_time:.2f}s")
        print()
        
        # Print status distribution
        print("📊 Status Verteilung:")
        for status, count in sorted(status_counts.items()):
            percentage = (count / total_tests * 100) if total_tests > 0 else 0
            print(f"   {status}: {count} ({percentage:.1f}%)")
        print()
        
        # Print category results
        print("📋 Ergebnisse nach Kategorien:")
        for category, results in sorted(category_results.items()):
            total = results['total']
            passed = results['passed']
            rate = (passed / total * 100) if total > 0 else 0
            print(f"   {category}: {passed}/{total} ({rate:.1f}%)")
        
        print("=" * 70)
    
    def list_available_categories(self):
        """Listet alle verfügbaren Testkategorien auf"""
        stats = self.test_case_provider.get_test_statistics()
        
        print("📋 Verfügbare Testkategorien:")
        print("-" * 40)
        for category, count in stats.items():
            if category != 'total':
                print(f"   • {category}: {count} Tests")
        print(f"\nGesamt: {stats['total']} Tests")


def main():
    """Hauptfunktion für die Testausführung"""
    tester = NewChatbotTester()
    
    if len(sys.argv) == 1:
        # Run all tests
        tester.run_all_tests()
    elif len(sys.argv) == 2:
        command = sys.argv[1].lower()
        
        if command == "--help" or command == "-h":
            print("🤖 Museum Guide Chatbot - Neue Tests")
            print("=" * 50)
            print("Verwendung:")
            print("  python new_test.py                    - Alle Tests ausführen")
            print("  python new_test.py [kategorie]        - Tests für Kategorie ausführen")
            print("  python new_test.py --list             - Verfügbare Kategorien anzeigen")
            print("  python new_test.py --help             - Diese Hilfe anzeigen")
            print()
            tester.list_available_categories()
            
        elif command == "--list" or command == "-l":
            tester.list_available_categories()
            
        else:
            # Try to run category tests
            if tester.run_category_tests(command):
                print("✅ Kategorie-Tests erfolgreich abgeschlossen")
            else:
                print("❌ Kategorie-Tests fehlgeschlagen")
                print("Verwenden Sie '--list' um verfügbare Kategorien zu sehen")
    else:
        print("❌ Ungültige Argumente. Verwenden Sie '--help' für Hilfe.")


if __name__ == "__main__":
    main()
