#!/usr/bin/env python3
"""
Modularized test script for the Museum Guide Chatbot
This script uses the new modular test architecture
"""

import sys
import os

# Add tests directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

from tests.test_cases import TestCaseProvider
from tests.utils.test_runner import TestRunner
from tests.utils.results_saver import ResultsSaver
from tests.config import SERVER_CONFIG


class ModularChatbotTester:
    """Main test orchestrator using modular components"""
    
    def __init__(self):
        self.test_case_provider = TestCaseProvider()
        self.test_runner = TestRunner()
        self.results_saver = ResultsSaver()
    def run_all_tests(self):
        """Runs the complete test suite"""
        print("🤖 Museum Guide Chatbot - Erweiterte Tests")
        print("=" * 60)
        
        # Get test cases
        test_cases = self.test_case_provider.get_all_test_cases()
        
        # Print statistics
        print(f"📊 Gesamt Testfälle: {len(test_cases)}")
        categories = {}
        for test in test_cases:
            category = test.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        
        print("📋 Kategorien:")
        for category, count in categories.items():
            print(f"   • {category}: {count} Tests")
        print("-" * 60)
        
        # Run tests
        test_results = self.test_runner.run_all_tests(test_cases)
        
        if test_results:
            # Save results
            results_file = self.results_saver.save_results(
                test_results, 
                self.test_runner.session_id,
                SERVER_CONFIG["url"]
            )
            
            print(f"\n💾 Ergebnisse gespeichert in: {results_file}")
        else:
            print("\n❌ Keine Tests durchgeführt (Server nicht verfügbar)")


def main():
    """Main function"""
    tester = ModularChatbotTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
